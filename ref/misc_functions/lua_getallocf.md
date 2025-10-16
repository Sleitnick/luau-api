---
name: lua_getallocf
ret: lua_Alloc
stack: "-0, +0, -"
args:
  - name: L
    type: lua_State*
    desc: Lua thread
  - name: ud
    type: void**
    desc: Userdata
---

Returns the memory allocator function, and writes the the opaque userdata pointer. These are the values that were originally passed to `lua_newstate`.

**Note:** `ud` is only written if the value was provided as non-null to `lua_newstate`. Beware of garbage values.

```cpp title="Example"
void* ud = nullptr; // Note: explicitly initalized as nullptr
lua_Alloc alloc_fn = lua_getallocf(L, &ud);
```
