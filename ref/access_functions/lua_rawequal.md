---
name: lua_rawequal
ret: int
stack: "-0, +0, -"
args:
  - name: L
    type: lua_State*
    desc: Lua thread
  - name: idx1
    type: int
    desc: Stack index
  - name: idx2
    type: int
    desc: Stack index
---

The same as `lua_equal`, except it does not call any metatable `__eq` functions.
