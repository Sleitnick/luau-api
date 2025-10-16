---
name: lua_stackdepth
ret: int
stack: "-0, +0, -"
args:
  - name: L
    type: lua_State*
    desc: Lua thread
---

Returns the current stack depth.
