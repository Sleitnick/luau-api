---
name: lua_topointer
ret: void*
stack: "-0, +0, -"
args:
  - name: L
    type: lua_State*
    desc: Lua thread
  - name: idx
    type: int
    desc: Stack index
---

Returns a pointer to the value at the given stack index. This works for userdata, lightuserdata, strings, tables, buffers, and functions.

**Note:** This should only be used for debugging purposes.

```cpp title="Example" hl_lines="4"
void* buf = lua_newbuffer(L, 10);

size_t len;
void* b = lua_tobuffer(L, -1, &len);
// b == buf
// len == 10
```
