---
name: luaL_checkvector
ret: const float*
stack: "-0, +0, -"
args:
  - name: L
    type: lua_State*
    desc: Lua thread
  - name: idx
    type: int
    desc: Stack index
---

Returns the vector at the given Luau index. If the value at the given index is not a vector, an error is thrown.
