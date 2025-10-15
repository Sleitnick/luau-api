---
name: lua_isyieldable
ret: int
stack: "-0, +0, -"
args:
  - name: L
    type: lua_State*
    desc: Lua thread
---

Returns `1` if the coroutine is yieldable, otherwise `0`.
