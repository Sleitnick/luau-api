---
name: lua_equal
ret: int
stack: "-0, +0, -"
args:
  - name: L
    type: lua_State*
    desc: Lua thread
  - name: idx1
    type: int
    desc: Stack index
  - name: idx2
    type: int
    desc: Stack index
---

Returns `1` if the values at `idx1` and `idx2` are equal. If applicable, this will call the `__eq` metatable function. Use `lua_rawequal` to avoid the metatable call. Returns `0` if the values are not equal (including if either of the indices are invalid).

```cpp title="Example" hl_lines="4"
lua_pushliteral(L, "hello");
lua_pushliteral(L, "hello");

if (lua_equal(L, -2, -1)) {
	printf("equal\n");
}
```
