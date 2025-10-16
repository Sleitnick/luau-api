---
name: luaL_checkunsigned
ret: unsigned
stack: "-0, +0, -"
args:
  - name: L
    type: lua_State*
    desc: Lua thread
  - name: idx
    type: int
    desc: Stack index
---

Returns the number (cast to `unsigned`) at the given stack index. If the value is not a number, an error is thrown.

```cpp title="Example"
int add_int(lua_State* L) {
	unsigned lhs = luaL_checkunsigned(L, 1);
	unsigned rhs = luaL_checkunsigned(L, 2);

	lua_pushunsigned(L, lhs + rhs);
	return 1;
}
```
