# Native Code Generation

Luau provides native code generation (NCG). This is a feature that must be explicitly enabled.

The first step to enable NCG is to check if it is supported, and then create the code generator state. We will do this with the `luau_codegen_supported` and `luau_codegen_create` functions. Luau must be built with Luau the CodeGen project for this to work.

## Enable

```cpp title="Enable NCG" hl_lines="3-5"
lua_State* L = luaL_newstate();

if (luau_codegen_supported()) {
    luau_codegen_create(L);
}

luaL_openlibs(L);
luaL_sandbox(L);
```

## Compile

Next, when you load your script for execution, call `luau_codegen_compile(L, idx)`, where `idx` is the location of our loaded script.

```cpp
int res = luau_load(script, ...);
if (res != 0) {
    // handle error
    return;
}

if (luau_codegen_supported()) {
    luau_codegen_compile(script, -1);
}
```

## Enable Within Luau

By default, our Luau code still won't compile to native code yet. There are two ways to enable NCG within our Luau code.

### Native Directive

By adding the `native` directive in our script, we signal to Luau that we would like the script to be natively compiled. Directives always go at the top of scripts and begin with `--!`.

```luau hl_lines="1"
--!native

local function buildVectors()
    local t = table.create(1024)
    for i = 1, 1024 do
        t[i] = vector.create(i, i, i)
    end
    return t
end

local function multiplyVectorsInPlace(vecs: { vector }, n: number)
    for i in vecs do
        vecs[i] *= n
    end
end

local vecs = buildVectors()
multiplyVectorsInPlace(vecs, 5)
```

### Native Function Attribute

Sometimes, it is undesirable to target native compilation for an entire script. Instead, it might be more beneficial to target specific functions. This can be done with the `@native` function attribute in Luau.

```luau hl_lines="3"
local function buildVectors() ... end

@native
local function multiplyVectorsInPlace(vecs: { vector }, n: number)
    for i in vecs do
        vecs[i] *= n
    end
end

local vecs = buildVectors()
multiplyVectorsInPlace(vecs, 5)
```

To clarify, the `@native` attribute can be on the same line as the function definition. Do whatever is clearer for you and your team. It is also not necessary for the function to be local.

```luau
@native local function a()
    -- ...
end

@native function b()
    -- ...
end
```

## IR Lowering

While NCG might give a boost for built-in Luau libraries and functions, there is no real gain for custom userdata types out of the box.

Luau includes APIs to generate IR (intermediate representation) code for userdata accesses, method calls, and some other metamethod calls. This may result in significant performance benefits.

## Profiling

NCG is not always going to be faster than normal Luau bytecode. As such, always profile and benchmark your code to understand if NCG is improving performance as expected. Experiment with directive-level and function-attribute-level NCG to understand which performs best for your code.
