---
name: luaL_checkbuffer
ret: void*
stack: "-0, +0, -"
args:
  - name: L
    type: lua_State*
    desc: Lua thread
  - name: idx
    type: int
    desc: Stack index
---

Returns the buffer at the given stack index. If the value retrieved is not a buffer, an error is thrown.
