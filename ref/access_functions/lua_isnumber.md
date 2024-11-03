---
name: lua_isnumber
ret: int
stack: "-0, +0, -"
args:
  - name: L
    type: lua_State*
    desc: Lua thread
  - name: idx
    type: int
    desc: Stack index
---

Returns `1` if the value at stack index `idx` is a number _or_ the value is a string that can be coerced to a number. Otherwise, returns `0`.
