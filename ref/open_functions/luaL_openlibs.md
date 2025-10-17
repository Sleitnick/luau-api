---
name: luaL_openlibs
ret: int
stack: "-0, +1, -"
args:
  - name: L
    type: lua_State*
    desc: Lua thread
---

Opens all built-in Luau libraries.

```cpp title="Example"
lua_State* L = luaL_newstate();
luaL_openlibs(L);
// ...
```
