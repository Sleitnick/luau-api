---
name: lua_getuserdatametatable
ret: void
stack: "-0, +1, -"
args:
  - name: L
    type: lua_State*
    desc: Lua thread
  - name: tag
    type: int
    desc: Tag
---

Pushes the metatable associated with the userdata tag onto the stack (or `nil` if there is no associated metatable).
