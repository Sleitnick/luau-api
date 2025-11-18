# Native Userdata

While Native Code Generation (NCG) might give a boost for built-in Luau libraries and functions, there is no real gain for custom userdata types out of the box.

Luau includes APIs to generate IR (intermediate representation) code for userdata accesses, method calls, and some other metamethod calls. This may result in significant performance benefits. The process of generating IR is often referred to as "IR Lowering." To generalize, you can think of IR code as the middleman between actual source code and native code. The IR code is then processed into native code. Thus, only one version of IR code must be generated, which then allows multiple native targets. In other words, you only need to write one IR generation for your userdata, rather than multiple native ones.

Note: Some of the code and examples are taken from the [`IrLowering`](https://github.com/luau-lang/luau/blob/7aba73849f1a6f98e1bcf77aea2fdf86e1551ab8/tests/IrLowering.test.cpp) conformance test.

## Setup

Using tagged userdata types is the first step in this whole process. Follow the [Userdata Tags](tags.md) guide for more info.

### Define Types

Next, we need to tell Luau the name of our userdata types. In this example, we'll build out a simple Vector2 userdata type. Thus, we'll define our null-terminated type array as such:

```cpp
static const char* kUserdataTypes[] = {
	"Vector2",
	nullptr,
};
```

We will also benefit from hard-coding the index for each value in our array. These do _not_ need to be the same value as the tag itself.

```cpp
constexpr uint8_t kVector2Type = 0;
```

### Remap

When we initially open up the Luau state and enable native codegen, we need to also assign a runtime userdata type remapper callback. This will essentially do the same thing as we hard-coded: get the index of a type within the `kUserdataTypes` array. See [this discussion](https://github.com/luau-lang/luau/discussions/1885#discussioncomment-13619460) for more info.

The code can look something like this:

```cpp
#include <Luau/CodeGen.h>
#include <string_view>

Luau::CodeGen::create(L); // instead of luau_codegen_create(L)

// Map a type (str) to the expected index
Luau::CodeGen::setUserdataRemapper(
	L,
	kUserdataTypes,
	[](void* ctx, const char* str size_t len) -> uint8_t {
		const char** types = (const char**)ctx;
		uint8_t idx = 0;
		std::string_view sv{str, len};

		for (; *types; ++types) {
			if (sv == *types) {
				return idx;
			}
			idx++;
		}

		// For failed matches, we must return 0xff:
		return 0xff;
	}
)
```

## Normal Compilation

We first need to add the `kUserdataTypes` array to our Luau compilation options struct.

```cpp hl_lines="4"
lua_CompileOptions options{};
// ... other options

options.userdataTypes = kUserdataTypes;

// ...
char data = luau_compile(source, source_len, &options, &data_len);
```

## Native Compilation

In the [Native](native.md) guide, we used the Luau API `luau_codegen_compile` function. Unfortunately, that function does not allow us to pass NCG options. Thus, we will need to use the Luau namespace within the Luau CodeGen library instead: `Luau::CodeGen::compile(...)`.

Just like before, we call this after our code has been loaded with `luau_load`.

```cpp
int res = luau_load(L, ...);
// ...handle res

if (Luau::CodeGen::isSupported()) {
	Luau::CodeGen::CompilationOptions native_opts{};

	// Assign our userdata types here too, which helps in better codegen:
	native_opts.userdataTypes = kUserdataTypes;

	// ...other options (we'll cover them next)

	Luau::CodeGen::compile(L, -1, native_opts);
}
```

Note that we assign our same `kUserdataTypes` array to the native compilation options too. Optionally, the return type of `compile` (`Luau::CodeGen::CompilationResult`) can also be captured to inspect the result of the compilation.

## IR Generation

Now comes the fun part. We need to instruct Luau on two fronts: (1) what Luau type is expected for a given field, and (2) what IR code should be generated.

For the sake of simplicity, we will only focus on accessing the "x" and "y" properties of a custom Vector2 userdata. Let's assume the backing struct for this userdata looks like this:

```cpp
struct Vector2 {
	float x;
	float y;
}
```

Also note that this does _not_ replace your standard code for interfacing with userdata, such as creating a metatable and assigning metamethods.

### Access Type

The first step is to tell Luau what bytecode type to expect when accessing our Vector2. This is done through the `userdataAccessBytecodeType` callback on the native compilation options struct.

Here's a stub for our first callback:

```cpp
#include <Luau/Bytecode.h>

uint8_t ud_access_bytecode_type(uint8_t type, const char* member, size_t member_len) {
	// Fallback to "any" type:
	return LBC_TYPE_ANY;
}
```

We need to assign this callback to our native code generation options:

```cpp
native_opts.userdataAccessBytecodeType = ud_access_bytecode_type;
```

Before we start filling out our callback, we first need to write a couple of functions to map between our userdata index (e.g. `kIrVector2`) and the type index Luau uses (which is just an offset from `LBC_TYPE_TAGGED_USERDATA_BASE`). These two helper functions will look like this:

```cpp
static inline uint8_t type_to_ud_idx(uint8_t type) {
	return type - LBC_TYPE_TAGGED_USERDATA_BASE;
}

static inline uint8_t ud_idx_to_type(uint8_t ud_idx) {
	return LBC_TYPE_TAGGED_USERDATA_BASE + ud_idx;
}
```

Within our callback, we need to tell Luau that our "x" and "y" properties should be typed as numbers (`LBC_TYPE_NUMBER`).

```cpp
uint8_t ud_access_bytecode_type(uint8_t type, const char* member, size_t member_len) {
	switch (type_to_ud_idx(type)) {
	case kIrVector2:
		if (strcmp(member, "x") == 0 || strcmp(member, "y") == 0) {
			return LBC_TYPE_NUMBER;
		}
		break;
	
	default:
		break;
	}

	return LBC_TYPE_ANY;
}
```

When Luau sees "vec2.x" (and when it knows vec2 is a Vector2 from the given type), then our callback will inform Luau that the expected access type is a number.

### IR Builder

Our final step is to generate the necessary intermediate code for our "x" and "y" properties.

Let's write our stub first:

```cpp
bool ud_access(
	IrBuilder& build,
	uint8_t type,
	const char* member,
	size_t member_len,
	int result_reg,
	int source_reg,
	int pcpos
) {
	// We return 'false' if no IR code is generated:
	return false;
}
```

Assign the callback to the native options, just like our previous callback:

```cpp
native_opts.userdataAccess = ud_access;
```

Our next chunk of code will be the most complicated, as we're interfacing with Luau's `IrBuilder`. The various commands are documented in Luau's CodeGen [`IrData.h`](https://github.com/luau-lang/luau/blob/master/CodeGen/include/Luau/IrData.h) header. Other than that, there is not much documentation outside of just reading the source code.

The gist of what we want to do is:

1. Load our userdata value from the `source_reg` VM register.
2. Run a check to ensure the value is indeed our Vector2-tagged userdata.
3. Read the "x" or "y" float property.
4. Store the result and type into the `result_reg` VM registry.

Let's write the code for reading "x" first. The code for "y" will be almost identical, other than the offset into our data struct.

```cpp
void gen_ir_vector2_x(IrBuilder& build, int result_reg, source_reg, int pcpos) {
	// Load the userdata
	IrOp udata = build.inst(IrCmd::LOAD_POINTER, build.vmReg(source_reg));

	// Check that our userdata is a Vector2 using our tag
	// (This assumes `kVector2Tag` is the tag value)
	build.inst(IrCmd::CHECK_USERDATA_TAG, udata, build.constInt(kVector2Tag), build.vmExit(pcpos));

	// Load the value (note the 'offsetof' macro, grabbing the proper offset to 'x' in 'Vector2')
	IrOp value = build.inst(IrCmd::BUFFER_READF32, udata, build.constInt(offsetof(Vector2, x)), build.constTag(LUA_TUSERDATA));

	// Store the value of 'x' into the result register:
	build.inst(IrCmd::STORE_DOUBLE, build.vmReg(result_reg), value);

	// Store the type of 'x' into the result register:
	build.inst(IrCmd::STORE_TAG, build.vmReg(result_reg), build.constTag(LUA_TNUMBER));
}

bool ud_access(
	IrBuilder& build,
	uint8_t type,
	const char* member,
	size_t member_len,
	int result_reg,
	int source_reg,
	int pcpos
) {
	switch (type_to_ud_idx(type)) {
	case kIrVector2:
		if (strcmp(member, "x") == 0) {
			gen_ir_vector2_x(build, result_reg, source_reg, pcpos);
			return true;
		}
		if (strcmp(member, "y") == 0) {
			gen_ir_vector2_y(build, result_reg, source_reg, pcpos);
			return true;
		}
		break;
	
	default:
		break;
	}
	return false;
}
```

We've made it! Now, when a Vector2's "x" property is accessed, Luau should properly generate the necessary IR code to fetch the property. The code for accessing "y" looks identical, except the `offsetof` macro references the "y" property instead: `offsetof(Vector2, y)`.

## Metamethods and Namecalls

We looked at "access" calls, e.g. accessing `Vector2.x`, but we skipped metamethod calls (`vec1 + vec2`) and namecalls (`vec1:Dot(vec2)`). These both have similar callbacks to the accessor callbacks. There are also similar callbacks for the builtin `vector` type. Including examples for all of these would be lengthy and repetitive. Instead, take a look at the [`ConformanceIrHooks.h`](https://github.com/luau-lang/luau/blob/7aba73849f1a6f98e1bcf77aea2fdf86e1551ab8/tests/ConformanceIrHooks.h) file for examples of all of these callbacks.

## Caveats

1. This only applies to natively generated code.
2. The type of the value must be known in the source code.
```luau
--!native

local function doThis(vec)
	print(vec.x) -- "vec" is "any" and thus no IR lowering is applied
end

local function doThat(vec: Vector2)
	print(vec.x) -- Receives IR-lowering, as "vec" is known to be "Vector2"
end
```
