---
name: luaL_addstring
ret: void
stack: "-0, +0, -"
args:
  - name: B
    type: luaL_Buffer*
    desc: Lua string buffer
  - name: s
    type: const char*
    desc: String
---

Adds a string to a string buffer. If the length of the string is known, use `luaL_addlstring` instead.
