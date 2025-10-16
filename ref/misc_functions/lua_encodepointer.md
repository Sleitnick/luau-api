---
name: lua_encodepointer
ret: uintptr_t
stack: "-0, +0, -"
args:
  - name: L
    type: lua_State*
    desc: Lua thread
  - name: p
    type: uintptr_t
    desc: Pointer
---

Encodes a pointer.

```cpp title="Example" hl_lines="3"
lua_newtable(L);
const void* ptr = lua_topointer(L, -1);
uintptr_t encoded_ptr = lua_encodepointer(L, uintptr_t(ptr));
printf("Pointer: 0x%016llx\n", encoded_ptr);
```
