---
name: lua_break
ret: void
stack: "-0, +0, -"
args:
  - name: L
    type: lua_State*
    desc: Lua thread
---

Trigger a break (i.e. breakpoint). This is different than `lua_breakpoint`, which installs a breakpoint.
