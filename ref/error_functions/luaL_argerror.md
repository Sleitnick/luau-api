---
name: luaL_argerror
ret: l_noret
stack: "-0, +0, -"
args:
  - name: L
    type: lua_State*
    desc: Lua thread
  - name: narg
    type: int
    desc: Argument number
  - name: extramsg
    type: const char*
    desc: Extra message
---

Throws a Luau error with a templated error message for an incorrect argument.

```cpp title="Example" hl_lines="5-7"
int divide(lua_State* L) {
	double numerator = luaL_checknumber(L, 1);
	double denominator = luaL_checknumber(L, 2);

	if (denominator == 0) {
		luaL_argerror(L, 2, "cannot divide by zero");
	}

	lua_pushnumber(L, numerator / denominator);
	return 1;
}
```
