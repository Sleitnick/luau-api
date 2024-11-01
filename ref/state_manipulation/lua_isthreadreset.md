---
name: lua_isthreadreset
ret: int
stack: "-0, +0, -"
args:
  - name: L
    type: lua_State*
    desc: Lua thread
---

Checks if the Lua thread is reset.
