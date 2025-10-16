---
name: lua_getupvalue
ret: int
stack: "-0, +(0|1), -"
args:
  - name: L
    type: lua_State*
    desc: Lua thread
  - name: level
    type: int
    desc: Stack level
  - name: n
    type: int
    desc: Argument number
---

Pushes an upvalue to the stack, and returns its name. If not found, returns `NULL` and nothing is pushed to the stack.
