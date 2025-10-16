---
name: lua_istable
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

Checks if the value at the given stack index is a table.

```cpp title="Example"
if (lua_istable(L, -1)) { /* ... */ }
```
