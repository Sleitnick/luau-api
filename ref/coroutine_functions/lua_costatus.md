---
name: lua_costatus
ret: int
stack: "-0, +0, -"
args:
  - name: L
    type: lua_State*
    desc: Lua thread
---

Gets the coroutine status (`lua_CoStatus`) of a given thread.

```cpp title="lua_CoStatus"
// Copied from luau/VM/include/lua.h
enum lua_CoStatus {
    LUA_CORUN = 0, // running
    LUA_COSUS,     // suspended
    LUA_CONOR,     // 'normal' (it resumed another coroutine)
    LUA_COFIN,     // finished
    LUA_COERR,     // finished with error
};
```
