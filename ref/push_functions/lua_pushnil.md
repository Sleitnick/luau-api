---
name: lua_pushnil
ret: void
stack: "-0, +1, -"
args:
  - name: L
    type: lua_State*
    desc: Lua thread
---

Pushes `nil` to the Luau stack.

```cpp title="Example"
lua_pushnil(L);
```
