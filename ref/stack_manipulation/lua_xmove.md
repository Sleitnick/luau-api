---
name: lua_xmove
ret: void
stack: "-?, +?, -"
args:
  - name: from
    type: lua_State*
    desc: Lua thread
  - name: to
    type: lua_State*
    desc: Lua thread
  - name: n
    type: int
    desc: Number of items to move
---

Moves the top `n` elements in the `from` stack to the top of the `to` stack. This pops `n` values from the `from` stack and pushes `n` values to the `to` stack.

Note: Both `from` and `to` states must share the same global state (e.g. the main state created with `lua_newstate`).

```cpp title="Example" hl_lines="9"
// Assume we have lua_State* A and B, both starting with empty stacks.

// Add some items to 'A' stack:
lua_pushboolean(A, true);
lua_pushinteger(A, 10);
lua_pushliteral(A, "hello");

// Moves the top 2 values from 'A' to 'B' (e.g. '10' and 'hello')
lua_xmove(A, B, 2);

printf("%d\n", lua_gettop(A)); // 1 (just the 'true' value remains)
printf("%d\n", lua_gettop(B)); // 2 (the '10' and 'hello' values)
```
