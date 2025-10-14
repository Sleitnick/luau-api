---
name: lua_setfenv
ret: int
stack: "-1, +0, -"
args:
  - name: L
    type: lua_State*
    desc: Lua thread
  - name: idx
    type: int
    desc: Stack index
---

Sets the environment of the value at `idx` to the table on the top of the stack, and pops this top value. Returns `0` if the value at the given index is not an applicable type for setting an environment (e.g. a number), otherwise returns `1`.
