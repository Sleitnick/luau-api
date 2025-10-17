---
name: luaL_checkstack
ret: void
stack: "-0, +0, m"
args:
  - name: L
    type: lua_State*
    desc: Lua thread
  - name: size
    type: int
    desc: Desired stack size
  - name: msg
    type: const char*
    desc: Error message
---

Ensures the stack is large enough to hold `size` _more_ elements. This will only grow the stack, not shrink it. Throws an error if the stack cannot be resized to the desired size.

```cpp title="Example"
// Ensure there are at least 2 more slots on the stack:
luaL_checkstack(L, 2, "failed to grow stack for the two numbers");

lua_pushinteger(L, 10);
lua_pushinteger(L, 20);
```
