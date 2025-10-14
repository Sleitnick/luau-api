---
name: lua_settable
ret: void
stack: "-2, +0, -"
args:
  - name: L
    type: lua_State*
    desc: Lua thread
  - name: idx
    type: int
    desc: Stack index
---

Sets the value of a table index, e.g. `t[k] = v`, where `t` is located on the stack at `idx`, and the key and value are on the top of the stack.

```cpp title="Example" hl_lines="5"
lua_newtable(L);

lua_pushliteral(L, "hello");
lua_pushinteger(L, 50);
lua_settable(L, -3); // t.hello = 50
```
