---
name: lua_clonefunction
ret: void
stack: "-0, +1, -"
args:
  - name: L
    type: lua_State*
    desc: Lua thread
  - name: idx
    type: int
    desc: Stack index
---

Clones a Luau function at the given index and pushes the cloned function to the top of the stack.
