---
name: lua_setuserdatatag
ret: int
stack: "-0, +0, -"
args:
  - name: L
    type: lua_State*
    desc: Lua thread
  - name: idx
    type: int
    desc: Stack index
  - name: tag
    type: int
    desc: Tag
---

Sets the tag for userdata at stack index `idx`. Alternatively, the [`lua_newuserdatatagged`](#lua_newuserdatatagged) and [`lua_newuserdatataggedwithmetatable`](#lua_newuserdatataggedwithmetatable) functions can be used to assign the tag on userdata creation.
