---
name: lua_tonumber
ret: double
stack: "-0, +0, -"
args:
  - name: L
    type: lua_State*
    desc: Lua thread
  - name: idx
    type: int
    desc: Stack index
---

Returns the number at the given stack index. If the value on the stack is a string, Luau will attempt to convert the string to a number. Identical to [`lua_tonumberx`](#lua_tonumberx), without the last `isnum` argument.
