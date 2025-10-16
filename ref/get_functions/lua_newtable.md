---
name: lua_newtable
ret: void
stack: "-0, +1, -"
args:
  - name: L
    type: lua_State*
    desc: Lua thread
---

Pushes a new table onto the stack. This is equivalent to `lua_createtable(L, 0, 0)`.
