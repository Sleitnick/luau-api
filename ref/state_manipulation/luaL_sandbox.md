---
name: luaL_sandbox
ret: lua_State*
stack: "-0, +0, -"
args:
  - name: L
    type: lua_State*
    desc: Parent thread
---

Sandboxes the Luau state. All libraries, built-in metatables, and globals are set to read-only. This also activates "safeenv" (`lua_setsafeenv`) on the global table.

```cpp title="Example"
lua_State* L = luaL_newstate();
luaL_openlibs(L);

// Sandboxing AFTER libraries are open:
luaL_sandbox(L);
```
