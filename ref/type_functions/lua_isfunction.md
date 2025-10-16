---
name: lua_isfunction
ret: int
stack: "-0, +0, -"
args:
  - name: L
    type: lua_State*
    desc: Lua thread
  - name: idx
    type: int
    desc: Stack index
---

Checks if the value at the given stack index is a function.

```cpp title="Example"
if (lua_isfunction(L, -1)) { /* ... */ }
```
