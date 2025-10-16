---
name: lua_getcoverage
ret: void
stack: "-0, +0, -"
args:
  - name: L
    type: lua_State*
    desc: Lua thread
  - name: funcindex
    type: int
    desc: Function index
  - name: context
    type: void*
    desc: Context
  - name: callback
    type: lua_Coverage
    desc: Coverage callback function
---

Get coverage.
