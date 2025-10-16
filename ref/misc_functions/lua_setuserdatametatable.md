---
name: lua_setuserdatametatable
ret: void
stack: "-1, +0, -"
args:
  - name: L
    type: lua_State*
    desc: Lua thread
  - name: tag
    type: int
    desc: Tag
---

Pops the value (expecting a table) at the top of the stack and sets the userdata metatable for the given userdata tag. This is used in conjunction with [`lua_newuserdatataggedwithmetatable`](#lua_newuserdatataggedwithmetatable). See the example there.

This function can only be called once per tag. Calling this function again for the same tag will throw an error.
