---
name: lua_setsafeenv
ret: void
stack: "-0, +0, -"
args:
  - name: L
    type: lua_State*
    desc: Lua thread
  - name: idx
    type: int
    desc: Stack index
  - name: enabled
    type: int
    desc: Safe environment enabled
---

Sets the safe-env state of a thread. TODO.
