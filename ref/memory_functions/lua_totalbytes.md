---
name: lua_totalbytes
ret: size_t
stack: "-0, +0, -"
args:
  - name: L
    type: lua_State*
    desc: Lua thread
  - name: category
    type: int
    desc: Memory category
---

Retrieves the total bytes allocated by a given memory category (`0` is the default memory category). Call [`lua_setmemcat`](#lua_setmemcat) to assign a memory category for a given thread.

```cpp title="Example" hl_lines="7"
constexpr uint8_t kExampleMemCat = 10;

lua_State* T = lua_newthread(L);
lua_setmemcat(T, kExampleMemCat);
lua_newbuffer(T, 1024 * 10); // 10KB buffer

size_t total_bytes = lua_totalbytes(T, kExampleMemCat);
printf("total: %zu bytes\n", total_bytes);
```
