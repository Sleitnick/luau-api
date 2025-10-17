---
name: luaL_getmetatable
ret: int
stack: "-0, +1, -"
args:
  - name: L
    type: lua_State*
    desc: Lua thread
  - name: name
    type: const char*
    desc: Name
---

Attempts to get a metatable from the registry with the given name and pushes it to the stack. If no metatable is found, `nil` will be pushed to the stack. See [`luaL_newmetatable`](#lual_newmetatable).

```cpp title="Example" hl_lines="16-17"
struct Foo {};

Foo* new_Foo() {
	Foo* foo = static_cast<Foo*>(lua_newuserdata(L, sizeof(Foo)));
	if (luaL_newmetatable(L, "Foo")) {
		// Build metatable:
		lua_pushliteral(L, "Foo");
		lua_rawsetfield(L, -2, "__type");
	}
	lua_setmetatable(L, -2);
	return foo;
}

// ...

// Get the metatable created with `luaL_newmetatable`:
luaL_getmetatable(L, "Foo");
```
