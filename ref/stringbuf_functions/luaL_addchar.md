---
name: luaL_addchar
ret: void
stack: "-0, +0, -"
args:
  - name: B
    type: luaL_Buffer*
    desc: Lua string buffer
  - name: c
    type: char
    desc: Character
---

Adds a character to a string buffer.
