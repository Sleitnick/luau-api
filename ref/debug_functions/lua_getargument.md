---
name: lua_getargument
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

Gets argument `n` at the given stack level. If found, the value is pushed to the top of the stack and the function returns `1`. Otherwise, the function returns `0` and nothing is pushed to the stack.
