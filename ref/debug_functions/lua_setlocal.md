---
name: lua_setlocal
ret: int
stack: "-(0|1), +0, -"
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

Sets a local variable at the given stack level to the value at the top of the stack. The name of the local variable is returned, and the value on the stack is popped. If no local is found, `NULL` is returned and nothing is popped from the stack.
