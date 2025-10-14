---
name: lua_tothread
ret: lua_State*
stack: "-0, +0, -"
args:
  - name: L
    type: lua_State*
    desc: Lua thread
  - name: idx
    type: int
    desc: Stack index
---

Returns the Luau thread at the given stack index, or `NULL` if the value is not a Luau thread.

```cpp title="Example" hl_lines="2"
lua_State* T = lua_newthread(L); // pushes T onto L's stack
lua_State* thread = lua_tothread(L, -1); // retrieve T from L's stack
// thread == T
```
