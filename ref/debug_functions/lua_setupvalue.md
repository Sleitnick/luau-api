---
name: lua_setupvalue
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

Pops a value off the stack and sets the given upvalue with the popped value, and returns its name. If not found, returns `NULL` and nothing is popped from the stack.
