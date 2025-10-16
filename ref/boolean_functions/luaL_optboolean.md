---
name: luaL_optboolean
ret: int
stack: "-0, +0, -"
args:
  - name: L
    type: lua_State*
    desc: Lua thread
  - name: idx
    type: int
    desc: Stack index
  - name: def
    type: int
    desc: Default
---

Returns `1` or `0` for the given boolean value. Returns `def` if the value at the given index is nil or none. Otherwise, an error is thrown.

**Note:** Unlike `lua_toboolean`, this is not a _truthy/falsey_ check. The value at the given index must be a boolean.
