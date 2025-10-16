---
name: lua_ref
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

Creates a reference to the given Luau value at `idx` on the stack. The returned integer can be seen as an opaque handle to the value. Creating a reference is also an easy way to pin a Luau value, preventing it from being GC'd. A reference can be created for any value on the stack. Attempting to create a reference to a nil value will return `LUA_REFNIL`.

Be sure to call [`lua_unref`](#lua_unref) when done with the reference. Call [`lua_getref`](#lua_getref) to retrieve the referenced value.

**Note:** Unlike in Lua, Luau does _not_ modify the stack when creating a reference. The stack remains the same.

```cpp title="Example" hl_lines="2"
lua_newtable(L);
int table_ref = lua_ref(L, -1);
lua_pop(L, 1);
// GC won't clean up the table, even though it was popped, becase a reference
// has been created for the table.
```
