---
name: lua_pushnumber
ret: void
stack: "-0, +1, -"
args:
  - name: L
    type: lua_State*
    desc: Lua thread
  - name: n
    type: double
    desc: Number
---

Pushes `n` to the stack.

```cpp title="Example"
lua_pushnumber(L, 15.2);
```
