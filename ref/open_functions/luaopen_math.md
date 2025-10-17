---
name: luaopen_math
ret: int
stack: "-0, +1, -"
args:
  - name: L
    type: lua_State*
    desc: Lua thread
---

Opens the math library. Use [`luaL_openlibs`](#lual_openlibs) to open all built-in Luau libraries, including this one.
