---
name: lua_rawsetfield
ret: void
stack: "-1, +0, -"
args:
  - name: L
    type: lua_State*
    desc: Lua thread
  - name: idx
    type: int
    desc: Stack index
  - name: k
    type: const char*
    desc: Field
---

The same as [`lua_setfield`](#lua_setfield), except no metamethods are invoked.
