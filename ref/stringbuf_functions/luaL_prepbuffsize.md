---
name: luaL_prepbuffsize
ret: char*
stack: "-0, +0, -"
args:
  - name: B
    type: luaL_Buffer*
    desc: Lua string buffer
  - name: size
    type: size_t
    desc: Size extension
---

Ensure the string buffer has at least `size` capacity available. For instance, if 10 characters need to be added to an existing string buffer, it may be more optimal to call `luaL_prepbuffsize(&b, 10)` before adding each character.
