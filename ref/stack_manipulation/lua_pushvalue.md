---
name: lua_pushvalue
ret: void
stack: "-0, +1, -"
args:
  - name: L
    type: lua_State*
    desc: Lua thread
  - name: idx
    type: int
    desc: Stack index
---

Pushes a copy of the value at index `idx` to the top of the stack.
