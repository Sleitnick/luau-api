---
name: lua_setmetatable
ret: int
stack: "-1, +0, -"
args:
  - name: L
    type: lua_State*
    desc: Lua thread
  - name: idx
    type: int
    desc: Stack index
---

Takes the table at the top of the stack and assigns it as the metatable of the table on the stack at `idx`.

The return value can be ignored; this function always returns `1`.

```cpp title="Example" hl_lines="7"
// Create table:
lua_newtable(L); // t

// Create metatable:
lua_newtable(L); // mt
lua_pushliteral("v");
lua_rawsetfield(L, -2, "__mode"); // mt.__mode = "v"
lua_setmetatable(L, -2); // setmetatable(t, mt)
```
