---
name: lua_tobuffer
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

Returns the buffer at the given stack index, or `NULL` if the value is not a buffer.

```cpp title="Example" hl_lines="4"
void* buf = lua_newbuffer(L, 10);

size_t len;
void* b = lua_tobuffer(L, -1, &len);
// b == buf
// len == 10
```
