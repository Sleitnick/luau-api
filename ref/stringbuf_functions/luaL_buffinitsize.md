---
name: luaL_buffinitsize
ret: char*
stack: "-0, +0, -"
args:
  - name: L
    type: lua_State*
    desc: Lua thread
  - name: B
    type: luaL_Buffer*
    desc: Lua string buffer
  - name: size
    type: size_t
    desc: Preallocated size
---

Initializes a string buffer with an initial allocated size. A pointer to the start of the buffer is returned.

```cpp title="Example"
luaL_Strbuf b;
char* buf = luaL_buffinitsize(L, &b, 512);
```
