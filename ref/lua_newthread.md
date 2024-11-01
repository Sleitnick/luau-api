---
name: lua_newthread
ret: lua_State*
stack: "-0, +1, -"
args:
  - name: L
    type: lua_State*
    desc: Parent thread
---

Creates a new Luau thread.
