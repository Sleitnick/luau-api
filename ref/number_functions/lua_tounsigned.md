---
name: lua_tounsigned
ret: unsigned
stack: "-0, +0, -"
args:
  - name: L
    type: lua_State*
    desc: Lua thread
  - name: idx
    type: int
    desc: Stack index
---

Returns the number at the given stack index as an unsigned integer. If the value on the stack is a string, Luau will attempt to convert the string to an integer. Numbers in Luau are all doubles, so the returned value is cast to an unsigned int. Identical to [`lua_tounsignedx`](#lua_tounsignedx), without the last `isnum` argument.
