---
name: lua_setfield
ret: void
stack: "-1, +0, -"
args:
  - name: L
    type: lua_State*
    desc: Lua thread
  - name: idx
    type: int
    desc: Stack index
  - name: k
    type: const char*
    desc: Field
---

Sets the value of a table index, e.g. `t[k] = v`, where `t` is located on the stack at `idx`, and the value is on the top of the stack.

```cpp title="Example" hl_lines="4"
lua_newtable(L);

lua_pushinteger(L, 50);
lua_setfield(L, -2, "hello"); // t.hello = 50
```
