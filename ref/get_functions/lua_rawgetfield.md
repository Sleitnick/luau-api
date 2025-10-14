---
name: lua_rawgetfield
ret: int
stack: "-0, +1, -"
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

This is the same as [`lua_getfield`](#lua_getfield), except no `__index` metamethod is ever called.
