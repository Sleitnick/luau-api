---
name: luaL_buffinit
ret: void
stack: "-0, +0, -"
args:
  - name: L
    type: lua_State*
    desc: Lua thread
  - name: B
    type: luaL_Buffer*
    desc: Lua string buffer
---

Initializes a string buffer.

```cpp title="Example"
luaL_Strbuf b;
luaL_buffinit(L, &b);
```
