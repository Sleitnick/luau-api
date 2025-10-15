---
name: lua_getthreaddata
ret: void*
stack: "-0, +0, -"
args:
  - name: L
    type: lua_State*
    desc: Lua thread
---

Gets data attached to the given thread. This is arbitrary data that is assigned with [`lua_setthreaddata`](#lua_setthreaddata).
