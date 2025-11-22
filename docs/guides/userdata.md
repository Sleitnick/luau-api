# Userdata

In Luau, userdata is a special type that allows you to create arbitrary data. This data is created and managed by Luau. We can even attach metatables to userdata to give them special behavior, such as properties and methods.

Through this guide, we will work our way toward building a full-featured userdata type, with a constructor, destructor, fields, methods, tags, atoms, and more.

Userdata is created with the `lua_newuserdata` function:

```cpp title="Create Userdata"
void* data = lua_newuserdata(L, 16); // Create userdata of 16 bytes
```

When we do this, Luau is allocating a chunk of memory for us. Importantly, Luau is managing this data; it is subject to removal by the garbage collector. Thus, holding onto a userdata without first [pinning](pinning.md) the value can be dangerous.

!!! note "Buffers"
	If all we need is just a chunk of arbitrary data managed by Luau, consider using [buffers](buffers.md) instead.

## Struct as Userdata

A common practice is to shape our userdata around a struct. This is as simple as creating a userdata with the same size as our struct and casting the value accordingly.

```cpp title="Userdata Struct"
struct Foo {
    int num;
    char* data;
    size_t data_size;
};

// Create userdata the same size as Foo and cast to Foo:
Foo* foo = static_cast<Foo*>(lua_newuserdata(L, sizeof(Foo)));

// Initialize fields:
foo->num = 0;
foo->data = nullptr;
foo->data_size = 0;
```

!!! warning "Zero-initialization"
	Luau gives us a chunk of memory, but it is _not_ zero-initialized. Ensure that you initialize all fields for your userdata, just as it's shown in the example above. C++'s placement new operator can be used as an easy way to zero-initialize, seen below.

Alternatively, C++'s placement new operator can be used to initialize data. This is a safe way to ensure your data is zero-initialized.

```cpp title="Placement New"
// Must include 'new' to use placement-new
#include <new>

// ...

Foo* foo = new (lua_newuserdata(L, sizeof(Foo))) Foo{};
// foo is zero-initialized, so no need to manually do so.
```

## Foo Library

Right now, we've simply shown code for creating userdata. But how can we expose this to Luau? Let's create a `Foo` library that contains a single `new` function. This will be our constructor. From Luau, we will be able to call `Foo.new()` to construct a new Foo object.

```cpp
// This is our Foo constructor
static int Foo_new(lua_State* L) {
    Foo* foo = static_cast<Foo*>(lua_newuserdata(L, sizeof(Foo)));
    foo->num = 0;
    foo->data = nullptr;
    foo->data_size = 0;
    return 1;
}

static const luaL_Reg foo_lib[] = {
    {"new", Foo_new},
    {nullptr, nullptr},
}

// Call this when we open other libraries on startup
void open_Foo(lua_State* L) {
    luaL_register(L, "Foo", foo_lib);
    lua_pop(L, 1);
}
```

From Luau, we can now construct Foo:

```luau
local foo = Foo.new()
print(type(foo)) -- "userdata"
```

That's great, but how do we give this purpose within our Luau code? It's meaningless at the moment. Luau code could figure out that it's a userdata value, but that's it. In order to give more behavior to our userdata, we need to attach a metatable. The metatable will describe what should happen when Luau code attempts to interact with Foo.

## Foo Metatable

We can see that Foo has a `num` field. Let's add a way to read and write this value from Luau, as well as handle methods. We can do this by assigning a metatable with the `__index`, `__newindex`, and `__namecall` fields pointing to our own custom functions.

First, let's create the metatable. Instead of simply creating a table and assigning it as a metatable, we're going to use the special `luaL_newmetatable` function. This function creates or fetches a table with a given name, which will allow us to do some more nifty tricks later.

```cpp
constexpr const char* kFooName = "Foo";

// Metamethod stubs:
static int Foo_index(lua_State* L) { /* ... */ }
static int Foo_newindex(lua_State* L) { /* ... */ }
static int Foo_namecall(lua_State* L) { /* ... */ }

// Map out our metatable:
static const luaL_Reg foo_mt[] = {
    {"__index", Foo_index},
    {"__newindex", Foo_newindex},
    {"__namecall", Foo_namecall},
    {nullptr, nullptr},
};

static int Foo_new(lua_State* L) {
    Foo* foo = static_cast<Foo*>(lua_newuserdata(L, sizeof(Foo)));
    // ...initialize foo fields

    // luaL_newmetatable returns true if the table was just created, thus we need
    // to populate its fields. It returns false if it already exists. In either case,
    // it is pushed to the stack.
    if (luaL_newmetatable(L, kFooName)) {
        // Assign our metatable functions:
        luaL_register(L, nullptr, foo_mt);

        // We can also assign a type, which is returned from Luau's "typeof" function:
        lua_pushliteral(L, "Foo");
        lua_rawsetfield(L, -2, "__type");
    }

    // Assign the metatable to our userdata:
    lua_setmetatable(L, -2);

    return 1;
}
```

## Read and Write

Now that we've set up our metatable, let's fill out our metamethods. We'll start with the `__index` handler.

```cpp
static int Foo_index(lua_State* L) {
    // Foo is at index 1 on the stack:
    Foo* foo = static_cast<Foo*>(lua_touserdata(L, 1));

    // The key is at index 2. We only want to allow string indexing, so we'll use checkstring:
    const char* key = luaL_checkstring(L, 2);

    // Access our "num" field:
    if (strcmp(key, "num") == 0) {
        lua_pushinteger(L, foo->num);
        return 1;
    }

    // Throw an error if the given key didn't match anything:
    luaL_error(L, "unknown property: %s", key);
}
```

From Luau, we can now read `num`:
```luau
local foo = Foo.new()
print(foo.num) -- 0
```

But we still can't write to `num`. Let's fix that. Our code within `Foo_newindex` will look similar to `Foo_index`, except we will have an extra argument on the stack (the value being set).

```cpp
static int Foo_newindex(lua_State* L) {
    Foo* foo = static_cast<Foo*>(lua_touserdata(L, 1));
    const char* key = luaL_checkstring(L, 2);

    // Access our "num" field:
    if (strcmp(key, "num") == 0) {
        int n = luaL_checkinteger(L, 3); // Ensure the argument is actually a number
        foo->num = n;
    }

    luaL_error(L, "unknown property: %s", key);
}
```

Our Luau code can now assign `num`:
```luau
local foo = Foo.new()
foo.num = 15
print(foo.num) -- 15
```

## Methods

We can assign methods to our userdata by utilizing the `__namecall` metatable field. When Luau calls a method (e.g. `foo:DoSomething()`), the `__namecall` metamethod will be triggered. We can use `lua_namecallatom` to fetch the name of the called method and figure out where to go from there. Let's fill out our `Foo_namecall` function to add a method for checking if the `num` field is even or odd.

We'll create a separate function for our actual method. This is just a matter of keeping things tidy (insert whatever code principle you want). It could be inlined, but that's not easily maintainable for a large collection of methods.

```cpp title="Method Handling"
static int Foo_IsNumEven(lua_State* L) { /* ... */ }

static int Foo_namecall(lua_State* L) {
    // The `nemcallatom` function grabs the method name being called. We are keeping
    // the `atom` argument null, but we'll come back to that later.
    const char* method = lua_namecallatom(L, nullptr);

    // Call our IsNumEven method:
    if (strcmp(method, "IsNumEven") == 0) {
        return Foo_IsNumEven(L);
    }

    luaL_error(L, "unknown method %s", method);
}
```

Our `Foo_IsNumEven` function will look like any other Luau C function. We'll grab Foo from its first position on the stack, and push a boolean indicating whether or not its `num` field is even.

```cpp title="IsEven Method"
static int Foo_IsNumEven(lua_State* L) {
    // Foo is at index 1. Any method arguments would come right after it.
    Foo* foo = static_cast<Foo*>(lua_touserdata(L, 1));

    lua_pushboolean(L, foo->num % 2 == 0);
    return 1;
}
```

Let's try it out from Luau:

```luau
local foo = Foo.new()

foo.num = 10
print(foo:IsNumEven()) -- true

foo.num = 7
print(foo:IsNumEven()) -- false
```

## Destructors

If our userdata value holds onto memory that we manage (e.g. we malloc a chunk of memory and store it in the userdata), then we need a way to free this memory when our userdata is freed by the garbage collector.

Luau allows us to bind a destructor function to our userdata. It's not very safe to access our Luau state from these destructors, but we can access our userdata value and free up any resources.

Note how our Foo struct has a `char* data` field. We haven't used this at all yet, but let's pretend we're using this field for some purpose.
```cpp
void create_data(Foo* foo, size_t size) {
    foo->data = new char[size];
    foo->data_size = size;
}
```

There are a couple ways we can bind a destructor to a userdata value. We'll look at `lua_newuserdatadtor` first, and look at the other way later on in this guide. This works just like our original `lua_newuserdata` function, except it accepts an additional destructor function argument. We'll just create this inline with a lambda function.

```cpp
static int Foo_new(lua_State* L) {
    Foo* foo = static_cast<Foo*>(lua_newuserdatadtor(L, sizeof(Foo), [](void* ptr) {
        // This function is called when the userdata is about to be GC'd.
        // The `ptr` parameter is our userdata.
        Foo* f = static_cast<Foo*>(ptr);

        // Free up resources
        delete[] f->data;
    }));

    // ...
}
```

## Other Metatable Fields

We are not limited to just `__index`, `__newindex`, and `__namecall`. We can use any of the metatable fields. Here is a non-exhaustive example of other metamethod fields for our Foo userdata:

```cpp
// __tostring
static int Foo_tostring(lua_State* L) {
    Foo* foo = static_cast<Foo*>(lua_touserdata(L, 1));
    lua_pushfstring(L, "Foo { num: %d, data_size: %zu }", foo->num, foo->data_size);
    return 1;
}

// __eq
static int Foo_eq(lua_State* L) {
    Foo* lhs = static_cast<Foo*>(lua_touserdata(L, 1));
    Foo* rhs = static_cast<Foo*>(lua_touserdata(L, 2));

    lua_pushboolean(
        L,
        lhs->num == rhs->num &&
        lhs->data_size == rhs->data_size &&
        memcmp(lhs->data, rhs->data, lhs->data_size) == 0
    );
}
```

## Improvements

### Tags

There are a few ways for us to improve on our existing code. One such improvements would be to utilize userdata tags. Check out the [Tags](tags.md) guide for a detailed overview on setting up userdata tags and why they are beneficial. When we use tags, this also frees us up to move our metatable construction and destructor assignment elsewhere at startup. We then get to use the longest function name in existence: `lua_newuserdatataggedwithmetatable` (new userdata, tagged, with metatable).

### Atoms

Another improvement is to use [Atoms](#atoms.md). Similar to tags, atoms assign unique numbers to strings, allowing us to do much quicker comparisons within our metamethods, e.g. deciding which method to use.
