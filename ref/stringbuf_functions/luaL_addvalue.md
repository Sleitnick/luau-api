---
name: luaL_addvalue
ret: void
stack: "-1, +0, -"
args:
  - name: B
    type: luaL_Buffer*
    desc: Lua string buffer
---

Pops a value from the top of the stack and adds it to the buffer.
