---
name: lua_rawseti
ret: int
stack: "-1, +0, -"
args:
  - name: L
    type: lua_State*
    desc: Lua thread
  - name: idx
    type: int
    desc: Stack index
  - name: n
    type: int
    desc: Table index
---

Performs `t[n] = v`, where `t` is the table on the stack at `idx`, and `v` is the value on the top of the stack. The top value is also popped.

```cpp title="Example" hl_lines="5"
lua_newtable(L);

for (int i = 1; i <= 10; i++) {
	lua_pushinteger(L, i * 10);
	lua_rawseti(L, -2, i); // t[i] = i * 10
}
```
