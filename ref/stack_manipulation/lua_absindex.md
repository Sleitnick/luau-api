---
name: lua_absindex
ret: int
stack: "-0, +0, -"
args:
  - name: L
    type: lua_State*
    desc: Lua thread
  - name: idx
    type: int
    desc: Index
---

Gets the absolute stack index. For example, if `idx` is `-2`, and the stack has 5 items, this function will return `4`.
