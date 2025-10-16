---
name: lua_getref
ret: int
stack: "-0, +1, -"
args:
  - name: L
    type: lua_State*
    desc: Lua thread
  - name: ref
    type: int
    desc: Reference
---

Retrieves the value from a given reference handle. The value is pushed to the top of the stack.

```cpp title="Example" hl_lines="5"
lua_newtable(L);
int table_ref = lua_ref(L, -1);

// Sometime later:
lua_getref(L, table_ref);
// Top of stack is now the table from the reference
```
