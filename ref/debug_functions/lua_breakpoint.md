---
name: lua_breakpoint
ret: int
stack: "-0, +0, -"
args:
  - name: L
    type: lua_State*
    desc: Lua thread
  - name: funcindex
    type: int
    desc: Function index
  - name: line
    type: int
    desc: Line
  - name: enabled
    type: int
    desc: Enabled
---

Enables or disables a breakpoint at the given line within the given function at `funcindex` on the stack.
