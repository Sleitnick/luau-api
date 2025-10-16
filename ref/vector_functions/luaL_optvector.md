---
name: luaL_optvector
ret: const float*
stack: "-0, +0, -"
args:
  - name: L
    type: lua_State*
    desc: Lua thread
  - name: idx
    type: int
    desc: Stack index
  - name: def
    type: const float*
    desc: Default
---

Returns the vector at the given Luau index. If the value at the given index is nil or none, then `def` is returned. Otherwise, an error is thrown.
