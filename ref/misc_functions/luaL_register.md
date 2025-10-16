---
name: luaL_register
ret: int
stack: "-0, +(0|1), -"
args:
  - name: L
    type: lua_State*
    desc: Lua thread
  - name: libname
    type: const char*
    desc: Library name
  - name: l
    type: const luaL_Reg*
    desc: Functions
---

Registers a library (i.e. a collection of functions within their own namespace). Internally, this is just a table of functions mapped by their associated key from `l`.

If `libname` is not null, the library is placed in the Luau registry and the new library table is pushed to the stack. Any Luau code will be able to access the library by name.

If `libname` is null, the function assumes a table is at the top of the stack, and will register all functions into that table.

```cpp title="Example" hl_lines="6-11 14"
// Library functions:
static int do_this(lua_State* L) { /* ... */ }
static int do_that(lua_State* L) { /* ... */ }

// Define library key/pairs:
static const luaL_Reg foo_lib[] = {
	// {Name, C Function}
	{"dothis", do_this},
	{"dothat", do_that},
	{nullptr, nullptr}, // End of list is denoted by null pair
};

void open_foo(lua_State* L) {
	luaL_register(L, "foo", foo_lib);
	lua_pop(L, 1); // luaL_register had left our library on the stack
}
```

```luau title="Luau Example"
-- Luau can now access "foo":
foo.dothis()
foo.dothat()
```

Alternatively, `luaL_register` can be used to write the functions to an already-existing table. For instance, a metatable:
```cpp title="Example Metatable" hl_lines="9-14 18"
constexpr int kFooTag = 10;

struct Foo {};

static int Foo_index(lua_State* L) { /* ... */ }
static int Foo_newindex(lua_State* L) { /* ... */ }
static int Foo_tostring(lua_State* L) { /* ... */ }

static const luaL_Reg foo_mt[] = {
	{"__index", Foo_index},
	{"__newindex", Foo_newindex},
	{"__tostring", Foo_tostring},
	{nullptr, nullptr},
};

void Foo_setup_metatable(lua_State* L) {
	luaL_newmetatable(L, "Foo");
	luaL_register(L, nullptr, foo_mt);
	lua_setuserdatametatable(L, kFooTag);
}
```
