---
name: lua_rawget
ret: int
stack: "-1, +1, -"
args:
  - name: L
    type: lua_State*
    desc: Lua thread
  - name: idx
    type: int
    desc: Stack index
---

This is the same as [`lua_gettable`](#lua_gettable), except no `__index` metamethod is ever called.
