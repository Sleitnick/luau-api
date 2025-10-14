---
name: lua_getfield
ret: int
stack: "-0, +1, -"
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

Pushes a value from a table onto the stack. The table is at index `idx` on the stack, and the key into the table is `k`. The `__index` metamethod may be triggered when using this function. If this is undesirable, use [`lua_rawgetfield`](#lua_rawgetfield) instead.

Returns the type of the value.

```cpp title="Example"
// Assume the top of the stack is the Luau table: { "hello" = 40 }
int t = lua_getfield(L, -2, "hello"); // Our key "hello" is at the top of the stack, and -2 is the table.
// t == LUA_TNUMBER
// lua_tonumber(L, -1) == 40
```
