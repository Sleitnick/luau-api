---
name: lua_getlocal
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

Gets a local variable at the given stack level and pushes the value onto the stack. The name of the local variable is returned, and the value on the stack is popped. If no local is found, `NULL` is returned and nothing is pushed to the stack.
