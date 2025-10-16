---
name: luaL_optunsigned
ret: unsigned
stack: "-0, +0, -"
args:
  - name: L
    type: lua_State*
    desc: Lua thread
  - name: idx
    type: int
    desc: Stack index
  - name: def
    type: unsigned
    desc: Default
---

Returns the number (cast to `unsigned`) at the given stack index, or the default number if the value at the stack index is not a number.
