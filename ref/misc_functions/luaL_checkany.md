---
name: luaL_checkany
ret: void
stack: "-0, +0, m"
args:
  - name: L
    type: lua_State*
    desc: Lua thread
  - name: narg
    type: int
    desc: Argument number
---

Asserts the value at the given index is any value (including `nil`). In other words, this asserts that the value is not none.
