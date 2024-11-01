---
name: lua_insert
ret: void
stack: "-1, +1, -"
args:
  - name: L
    type: lua_State*
    desc: Lua thread
  - name: idx
    type: int
    desc: Stack index
---

Moves the top stack element into the given index, shifting other values up first to give space. The element right under the top stack element becomes the new top element.

```cpp title="Example" hl_lines="15"
lua_pushboolean(L, true);
lua_pushinteger(L, 10);
lua_pushliteral(L, "hello");
lua_pushinteger(L, 20);

// Current stack order:
// [-4] true
// [-3] 10
// [-2] hello
// [-1] 20

// Move the top value (20) to index -3.
// The values below the top and above -3 are shifted up.
// e.g. the '10' and 'hello' are shifted up first.
lua_insert(L, -3);

// New stack order:
// [-4] true
// [-3] 20
// [-2] 10
// [-1] hello
```
