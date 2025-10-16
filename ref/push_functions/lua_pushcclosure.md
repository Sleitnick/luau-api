---
name: lua_pushcclosure
ret: void
stack: "-n, +1, -"
args:
  - name: L
    type: lua_State*
    desc: Lua thread
  - name: fn
    type: lua_CFunction
    desc: C Function
  - name: debugname
    type: const char*
    desc: Debug name
  - name: nup
    type: int
    desc: Number of upvalues to capture
---

Equivalent to `lua_pushcclosurek`, but without any continuation function provided.
