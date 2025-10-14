---
name: lua_rawgeti
ret: int
stack: "-1, +1, -"
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

Pushes the table value at index `n` onto the stack. The table is located on the stack at `idx`. Similar to `lua_rawget`, no metamethods are called. Note that Luau tables start at index `1`, not `0`.

```cpp title="Example" hl_lines="2"
// Assume the top of the stack is the Luau table: { 5, 15, 30 }
lua_rawgeti(L, -1, 2); // t[2]
double n = lua_tonumber(L, -1);
printf("%f\n", n); // 15
```
