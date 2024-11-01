---
name: lua_mainthread
ret: lua_State*
stack: "-0, +0, -"
args:
  - name: L
    type: lua_State*
    desc: Lua thread
---

Returns the main Lua state (e.g. the state created from `lua_newstate()`).
