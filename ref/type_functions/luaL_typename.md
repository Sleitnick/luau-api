---
name: luaL_typename
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

Returns the name of the type at the given index.

```cpp title="Example"
lua_pushvector(L, 10, 20, 30);
const char* t_name = luaL_typename(L, -1);
printf("Type: %s\n", t_name); // "Type: vector"
```
