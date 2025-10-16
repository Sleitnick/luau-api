---
name: luaL_checkboolean
ret: int
stack: "-0, +0, -"
args:
  - name: L
    type: lua_State*
    desc: Lua thread
  - name: idx
    type: int
    desc: Stack index
---

Returns `1` if the Luau value at the given stack index is true, otherwise returns `0`. Throws an error if the value at the given index is not a boolean.

**Note:** Unlike `lua_toboolean`, this is not a _truthy/falsey_ check. The value at the given index must be a boolean.
