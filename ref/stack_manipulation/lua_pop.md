---
name: lua_pop
ret: void
stack: "-n, +0, -"
args:
  - name: L
    type: lua_State*
    desc: Lua thread
  - name: n
    type: int
    desc: Number of items to pop
---

Pops `n` values off the top of the stack.

```cpp title="Example" hl_lines="8"
// Assume lua_gettop(L) == 0 here

lua_pushliteral(L, "Hello");
lua_pushnumber(L, 85.2);
lua_pushboolean(L, true);
printf("Size: %d\n", lua_gettop(L)); // Size: 3

lua_pop(L, 2);

printf("Size: %d\n", lua_gettop(L)); // Size: 1
printf("Type: %s\n", luaL_typename(L, -1)); // string (top of stack is the "Hello" value now)
```
