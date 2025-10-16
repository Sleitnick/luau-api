---
name: lua_tostring
ret: const char*
stack: "-0, +0, -"
args:
  - name: L
    type: lua_State*
    desc: Lua thread
  - name: idx
    type: int
    desc: Stack index
---

Equivalent to [`lua_tolstring`](#lua_tolstring), without the length argument.
