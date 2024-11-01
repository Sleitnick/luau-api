---
name: lua_remove
ret: void
stack: "-1, +0, -"
args:
  - name: L
    type: lua_State*
    desc: Lua thread
  - name: idx
    type: int
    desc: Stack index
---

Removes the value at the given stack index `idx`. All other values above the index are shifted down.

```cpp title="Example" hl_lines="5"
lua_pushinteger(L, 10);
lua_pushboolean(L, true);
lua_pushliteral(L, "hello");

lua_remove(L, -2); // remove the 'true' value.

printf("%s\n", luaL_tostring(L, -2)); // 'hello'
```
