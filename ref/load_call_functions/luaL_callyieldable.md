---
name: luaL_callyieldable
ret: int
stack: "-(nargs + 1), +nresults, -"
args:
  - name: L
    type: lua_State*
    desc: Lua thread
  - name: nargs
    type: int
    desc: Number of arguments
  - name: nresults
    type: int
    desc: Number of returned values
---

Similar to `lua_call`, except this function can call yieldable C functions.

Returns the status of the call. If the call was a C function and the C function yielded, this will be `-1`.
