---
name: lua_checkstack
ret: int
stack: "-0, +0, m"
args:
  - name: L
    type: lua_State*
    desc: Lua thread
  - name: size
    type: int
    desc: Desired stack size
---

TODO