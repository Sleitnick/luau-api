---
name: lua_rawgetptagged
ret: void
stack: "-0, +1, -"
args:
  - name: L
    type: lua_State*
    desc: Lua thread
  - name: idx
    type: int
    desc: Stack index
  - name: p
    type: void*
    desc: Arbitrary pointer to be represented as lightuserdata
---

Assuming table `t` on the stack at `idx`, this pushes to the stack `t[p]`.

```cpp title="Example" hl_lines="8-9"
struct SomeData {};
SomeData* data = new SomeData();

lua_newtable(L);
lua_pushliteral(L, "hello");
lua_rawsetptagged(L, -2, data); // t[data] = "hello"

lua_rawgetptagged(L, -1, data); // v = t[data]
const char* s = lua_tostring(L, -1); // "hello"
```
