---
name: luaL_optstring
ret: const char*
stack: "-0, +0, -"
args:
  - name: L
    type: lua_State*
    desc: Lua thread
  - name: idx
    type: int
    desc: Stack index
  - name: def
    type: const char*
    desc: Default string
---

Equivalent to [`luaL_optlstring(L, idx, def, nullptr)`](#lual_optlstring).
