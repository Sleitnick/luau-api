---
name: luaL_traceback
ret: void
stack: "-0, +1, -"
args:
  - name: L
    type: lua_State*
    desc: Lua thread
  - name: L1
    type: lua_State*
    desc: Lua thread
  - name: msg
    type: const char*
    desc: Message
  - name: level
    type: int
    desc: Stack level
---

Pushes a string onto the stack containing the traceback. The `msg` argument is the prefix for the traceback.
