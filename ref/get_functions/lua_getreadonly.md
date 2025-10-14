---
name: lua_getreadonly
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

Returns `1` if the table is marked as read-only, otherwise `0`.

```cpp title="Example" hl_lines="4"
// Assume a table is at the top of the stack
if (!lua_getreadonly(L, -1)) {
	// Safe to modify table
}
```
