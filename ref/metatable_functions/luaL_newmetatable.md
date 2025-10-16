---
name: luaL_newmetatable
ret: int
stack: "-1, +0, -"
args:
  - name: L
    type: lua_State*
    desc: Lua thread
  - name: name
    type: const char*
    desc: Name
---

Creates (or fetches existing) metatable with a given name and pushes the metatable onto the stack. Returns `1` if the metatable was created, or `0` if the metatable aleady exists. This is useful for creating metatables linked to specific userdata types.

```cpp title="Example" hl_lines="5"
struct Foo {};

Foo* foo = static_cast<Foo*>(lua_newuserdata(L, sizeof(Foo)));

if (luaL_newmetatable(L, "Foo")) {
	// Build metatable:
	lua_pushliteral(L, "Foo");
	lua_rawsetfield(L, -2, "__type");
}
lua_setmetatable(L, -2);
```
