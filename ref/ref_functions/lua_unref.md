---
name: lua_unref
ret: void
stack: "-0, +0, -"
args:
  - name: L
    type: lua_State*
    desc: Lua thread
  - name: ref
    type: int
    desc: Reference
---

Removes a reference that was originally created with `lua_ref`. Passing in `LUA_REFNIL` or `LUA_NOREF` is allowed (in those cases, the function does nothing). However, passing in an already-removed reference is _not_ allowed and may throw an error, or silently remove another reference. If idempotence is required, ensure your reference variable is set to `LUA_REFNIL` or `LUA_NOREF` after calling `lua_unref`.

```cpp title="Example" hl_lines="5"
lua_newtable(L);
int table_ref = lua_ref(L, -1);

// Sometime later:
lua_unref(L, table_ref);
```
