---
name: lua_iscfunction
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

Returns `1` if the value at the given stack index is a C function. Otherwise, returns `0`.
