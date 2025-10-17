---
name: lua_pushfstring
ret: const char*
stack: "-0, +1, -"
args:
  - name: L
    type: lua_State*
    desc: Lua thread
  - name: fmt
    type: const char*
    desc: C-style string for formatting
  - name: ...
    type: ""
    desc: Format arguments
---

Pushes a string to the stack, where the string is `fmt` formatted against the arguments. The formatted string is also returned.

```cpp title="Example"
const char* s = lua_pushfstring(L, "number: %d", 32);
```
