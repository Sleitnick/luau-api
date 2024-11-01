---
name: luaL_newstate
ret: lua_State*
stack: "-0, +0, -"
args:
---

A simplified version of `lua_newstate` that uses the default allocator, which uses the standard `free` and `realloc` memory functions.
