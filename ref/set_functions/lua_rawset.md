---
name: lua_rawset
ret: void
stack: "-2, +0, -"
args:
  - name: L
    type: lua_State*
    desc: Lua thread
  - name: idx
    type: int
    desc: Stack index
---

The same as [`lua_settable`](#lua_settable), except no metamethods are invoked.
