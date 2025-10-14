---
name: lua_gettable
ret: int
stack: "-1, +1, -"
args:
  - name: L
    type: lua_State*
    desc: Lua thread
  - name: idx
    type: int
    desc: Stack index
---

Pushes a value from a table onto the stack. The table is at index `idx` on the stack, and the key into the table is on the top of the stack. This function pops the key at the top of the stack. The `__index` metamethod may be triggered when using this function.  If this is undesirable, use [`lua_rawget`](#lua_rawget) instead.

Returns the type of the value.

```cpp title="Example"
// Assume the top of the stack is the Luau table: { "hello" = 40 }
lua_pushliteral(L, "hello");
int t = lua_gettable(L, -2); // Our key "hello" is at the top of the stack, and -2 is the table.
// t == LUA_TNUMBER
// lua_tonumber(L, -1) == 40
```
