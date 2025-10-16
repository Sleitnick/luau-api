---
name: luaL_checknumber
ret: double
stack: "-0, +0, -"
args:
  - name: L
    type: lua_State*
    desc: Lua thread
  - name: idx
    type: int
    desc: Stack index
---

Returns the number at the given stack index. If the value is not a number, an error is thrown.

```cpp title="Example"
int add(lua_State* L) {
	double lhs = luaL_checknumber(L, 1);
	double rhs = luaL_checknumber(L, 2);

	lua_pushnumber(L, lhs + rhs);
	return 1;
}
```
