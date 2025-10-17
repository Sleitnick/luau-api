---
name: luaL_addlstring
ret: void
stack: "-0, +0, -"
args:
  - name: B
    type: luaL_Buffer*
    desc: Lua string buffer
  - name: s
    type: const char*
    desc: String
  - name: l
    type: size_t
    desc: String length
---

Adds a string to a string buffer.
