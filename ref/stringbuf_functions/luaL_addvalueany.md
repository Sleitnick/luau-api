---
name: luaL_addvalueany
ret: void
stack: "-0, +0, -"
args:
  - name: B
    type: luaL_Buffer*
    desc: Lua string buffer
  - name: idx
    type: int
    desc: Stack index
---

Adds the value at the given stack index into the buffer. Unlike `luaL_addvalue`, this does _not_ pop the item from the stack.
