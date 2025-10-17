---
name: luaL_checkstring
ret: const char*
stack: "-0, +0, -"
args:
  - name: L
    type: lua_State*
    desc: Lua thread
  - name: idx
    type: int
    desc: Stack index
---

Equivalent to [`luaL_checklstring(L, idx, nullptr)`](#lual_checklstring).
