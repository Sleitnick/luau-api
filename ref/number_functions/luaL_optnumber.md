---
name: luaL_optnumber
ret: double
stack: "-0, +0, -"
args:
  - name: L
    type: lua_State*
    desc: Lua thread
  - name: idx
    type: int
    desc: Stack index
  - name: def
    type: double
    desc: Default
---

Returns the number at the given stack index, or the default number if the value at the stack index is not a number.

```cpp title="Example" hl_lines="5"
int approx_equal(lua_State* L) {
	double a = luaL_checknumber(L, 1);
	double b = luaL_checknumber(L, 2);

	double epsilon = luaL_optnumber(L, 3, 0.00001);

	lua_pushboolean(L, fabs(a - b) < epsilon);
	return 1;
}
```
