---
name: lua_pushlightuserdata
ret: void
stack: "-0, +1, -"
args:
  - name: L
    type: lua_State*
    desc: Lua thread
  - name: p
    type: void*
    desc: Pointer to arbitrary user-owned data
---

Pushes the tagged lightuserdata to the stack. Identical to `lua_pushlightuserdatatagged` with a tag of `0`.

```cpp title="Example" hl_lines="4"
struct Foo {};
Foo* foo = new Foo();

lua_pushlightuserdata(L, foo);
```
