---
name: lua_createtable
ret: void
stack: "-0, +1, -"
args:
  - name: L
    type: lua_State*
    desc: Lua thread
  - name: narr
    type: int
    desc: Array size
  - name: nrec
    type: int
    desc: Dictionary size
---

Pushes a new table onto the stack, allocating `narr` slots on the array portion and `nrec` slots on the dictionary portion. Use [`lua_newtable`](#lua_newtable) to create a table with zero size allocation, equivalent to `lua_createtable(0, 0)`.

These allocated slots are _not_ filled.

```cpp title="Example"
lua_createtable(L, 10, 0); // Push a new table onto the stack with 10 array slots allocated
// 10 slots allocated, but not filled, e.g. lua_objlen(L, -1) == 0
```
