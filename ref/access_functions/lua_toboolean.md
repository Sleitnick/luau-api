---
name: lua_toboolean
ret: int
stack: "-0, +0, -"
args:
  - name: L
    type: lua_State*
    desc: Lua thread
  - name: idx
    type: int
    desc: Stack index
---

Returns `1` if the Luau value at the given stack index is truthy, otherwise returns `0`.

A "falsey" value in Luau is any value that is either `nil` or `false`. All other values are evaluated as `true`. In other languages, values like `0` or empty strings might be evaluated as `false`. This is _not_ the case in Luau. _Only_ `nil` and `false` are evaluated as `false`; all other values are evaluated as `true`.

```cpp title="Example"
lua_pushboolean(L, true);
lua_pushboolean(L, false);
lua_pushnil(L);
lua_pushinteger(L, 0);

if (lua_toboolean(L, -4)) {} // true
if (lua_toboolean(L, -3)) {} // false
if (lua_toboolean(L, -2)) {} // false (nil is evaluated as false)
if (lua_toboolean(L, -1)) {} // true (0 is neither nil or false, so it is evaluated as true in Luau)
```
