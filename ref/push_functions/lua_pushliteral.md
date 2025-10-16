---
name: lua_pushliteral
ret: void
stack: "-0, +1, -"
args:
  - name: L
    type: lua_State*
    desc: Lua thread
  - name: str
    type: const char*
    desc: C-style string
---

Pushes the string literal `str` to the stack with a length of `len`.

```cpp title="Example"
lua_pushliteral(L, "hello world");
```
