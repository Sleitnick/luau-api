---
name: lua_isnoneornil
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

Checks if the value at the given stack index is none or nil.

```cpp title="Example"
if (lua_isnoneornil(L, -1)) { /* ... */ }
```
