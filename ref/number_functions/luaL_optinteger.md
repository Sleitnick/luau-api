---
name: luaL_optinteger
ret: int
stack: "-0, +0, -"
args:
  - name: L
    type: lua_State*
    desc: Lua thread
  - name: idx
    type: int
    desc: Stack index
  - name: def
    type: int
    desc: Default
---

Returns the number (cast to `int`) at the given stack index, or the default number if the value at the stack index is nil or none. Otherwise, an error is thrown.
