---
name: lua_settop
ret: int
stack: "-?, +?, -"
args:
  - name: L
    type: lua_State*
    desc: Lua thread
  - name: idx
    type: int
    desc: Top stack index
---

Sets the top of the stack, essentially resizing it to the given index. If the new size is larger than the current size, the new elements in the stack will be filled with `nil` values. Setting the stack size to 0 will clear the stack entirely.

```cpp
lua_settop(L, 0); // clear the stack
```
