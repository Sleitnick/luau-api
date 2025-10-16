---
name: luaL_checktype
ret: void
stack: "-0, +0, m"
args:
  - name: L
    type: lua_State*
    desc: Lua thread
  - name: narg
    type: int
    desc: Argument number
  - name: t
    type: int
    desc: Luau type
---

Asserts the type at the given index.

```cpp title="Example"
int do_something(lua_State* L) {
	// Assert that the first argument is a table:
	luaL_checktype(L, 1, LUA_TTABLE);
}
```
