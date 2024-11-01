---
name: lua_rawcheckstack
ret: void
stack: "-0, +0, m"
args:
  - name: L
    type: lua_State*
    desc: Lua thread
  - name: size
    type: int
    desc: Desired stack size
---

Similar to `lua_checkstack`, except it bypasses the max stack limit.
