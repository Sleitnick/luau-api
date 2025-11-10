---
name: lua_rawsetptagged
ret: void
stack: "-1, +0, -"
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

Assuming table `t` on the stack at `idx` and `v` at the top of the stack,
this pops `v` from the stack and adds it to the table: `t[p] = v`.

```cpp title="Example" hl_lines="4-6"
struct SomeData {};
SomeData* data = new SomeData();

lua_newtable(L);
lua_pushliteral(L, "hello");
lua_rawsetptagged(L, -2, data); // t[data] = "hello"
```
