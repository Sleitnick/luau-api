---
name: luaL_argcheck
ret: l_noret
stack: "-0, +0, -"
args:
  - name: L
    type: lua_State*
    desc: Lua thread
  - name: cond
    type: int
    desc: Condition
  - name: narg
    type: int
    desc: Argument number
  - name: extramsg
    type: const char*
    desc: Extra message
---

Throws a Luau error with a templated error message for an incorrect argument. This is similar to `luaL_argerror`, except it encapsulates a condition, similar to an assertion.

```cpp title="Example" hl_lines="5"
int divide(lua_State* L) {
	double numerator = luaL_checknumber(L, 1);
	double denominator = luaL_checknumber(L, 2);

	luaL_argcheck(L, denominator == 0, 2, "cannot divide by zero");

	lua_pushnumber(L, numerator / denominator);
	return 1;
}
```
