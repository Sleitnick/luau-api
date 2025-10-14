---
name: lua_setreadonly
ret: void
stack: "-0, +0, -"
args:
  - name: L
    type: lua_State*
    desc: Lua thread
  - name: idx
    type: int
    desc: Stack index
  - name: enabled
    type: int
    desc: Readonly enabled
---

Sets the read-only state of a table. Read-only tables ensure that table values cannot be modified, added, or removed. This is only a shallow application, i.e. a nested table may still be writable.

```cpp title="Example" hl_lines="4"
lua_newtable(L);
lua_pushliteral(L, "hello");
lua_rawsetfield(L, -2, "message"); // t.message = "hello"
lua_setreadonly(L, -1, true);
```
