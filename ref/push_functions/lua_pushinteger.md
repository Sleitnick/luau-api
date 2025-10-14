---
name: lua_pushinteger
ret: void
stack: "-0, +1, -"
args:
  - name: L
    type: lua_State*
    desc: Lua thread
  - name: n
    type: int
    desc: Number
---

Pushes `n` to the stack. Note that all Luau numbers are doubles, so the value of `n` will be cast to a `double`.

```cpp title="Example"
lua_pushinteger(L, 32);
```
