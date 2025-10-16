---
name: luaL_typeerror
ret: l_noret
stack: "-0, +0, -"
args:
  - name: L
    type: lua_State*
    desc: Lua thread
  - name: narg
    type: int
    desc: Argument number
  - name: tname
    type: const char*
    desc: Type name
---

Throws a Luau error with a templated error message for an incorrect type.

```cpp title="Example"
int send_table(lua_State* L) {
	// expects a table as the first argument
	if (!lua_istable(L, 1)) {
		luaL_typeerror(L, 1, "table"); // "invalid argument #1 to 'send_table' (table expected, got <TYPENAME>)"
	}

	// ...
}
```
