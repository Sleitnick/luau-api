---
name: lua_namecallatom
ret: const char*
stack: "-0, +0, -"
args:
  - name: L
    type: lua_State*
    desc: Lua thread
  - name: atom
    type: int*
    desc: Atom
---

When called within a `__namecall` metamethod, this function returns the name of the called method. An optional atom value can be utilized as well.

```cpp title="Example" hl_lines="6-14"
static constexpr const char* kFoo = "Foo";

struct Foo {};

// Handle namecalls, e.g. Luau calling "foo:Hello()"
static int Foo_namecall(lua_State* L) {
	const char* method = lua_namecallatom(L, nullptr);
	if (strcmp(method, "Hello") == 0) {
		// User called the 'Hello' method. Return "Goodbye":
		lua_pushliteral(L, "Goodbye");
		return 1;
	}
	luaL_error(L, "unknown method %s", method);
}

// Construct new Foo userdata:
int new_Foo(lua_State* L) {
	Foo* foo = static_cast<Foo*>(lua_newuserdata(L, sizeof(Foo)));
	if (luaL_newmetatable(L, kFoo)) {
		// Assign __namecall metamethod:
		lua_pushcfunction(L, Foo_namecall, "namecall");
		lua_rawsetfield(L, "__namecall", -2);
	}
	lua_setmetatable(L, -2);
	return 1;
}

static const luaL_Reg[] Foo_lib = {
	{"new", new_Foo},
	{nullptr, nullptr},
};

// Called from setup code for Luau state:
void open_Foo(lua_State* L) {
	lua_register(L, Foo_lib);
}
```
