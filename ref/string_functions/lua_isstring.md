---
name: lua_isstring
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

Returns `1` if the value at the given stack index is a string _or_ a number (all numbers can be converted to a string). Otherwise, returns `0`.
