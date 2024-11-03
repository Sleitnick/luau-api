---
name: lua_lessthan
ret: int
stack: "-0, +0, -"
args:
  - name: L
    type: lua_State*
    desc: Lua thread
  - name: idx1
    type: int
    desc: Stack index
  - name: idx2
    type: int
    desc: Stack index
---

Returns `1` if the value at `idx` is less than the value at `idx2`. Otherwise, returns `0`. This may call the `__lt` metamethod function. Also returns `0` if either index is invalid.
