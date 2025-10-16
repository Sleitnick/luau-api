---
name: lua_pushboolean
ret: void
stack: "-0, +1, -"
args:
  - name: L
    type: lua_State*
    desc: Lua thread
  - name: b
    type: int
    desc: Boolean
---

Pushes boolean `b` to the stack.

```cpp title="Example"
lua_pushboolean(L, true);
lua_pushboolean(L, false);
```
