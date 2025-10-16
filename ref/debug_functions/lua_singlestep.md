---
name: lua_singlestep
ret: int
stack: "-0, +0, -"
args:
  - name: L
    type: lua_State*
    desc: Lua thread
  - name: enabled
    type: int
    desc: Enabled
---

Enables or disables single-step mode.
