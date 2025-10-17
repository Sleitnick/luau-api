---
name: luaL_tolstring
ret: const char*
stack: "-0, +1, -"
args:
  - name: L
    type: lua_State*
    desc: Lua thread
  - name: idx
    type: int
    desc: Stack index
  - name: len
    type: size_t
    desc: String length
---

Converts the value at the given index into a string. This string is both pushed onto the stack and returned. Unlike `lua_tolstring` and `lua_tostring`, this function does _not_ modify the value at the given stack index.

```cpp title="Example" hl_lines="2"
lua_pushvector(L, 10, 20, 30);
const char* vstr = lua_tolstring(L, -1, nullptr);
lua_pop(L, 1); // pop vstr from the stack
printf("vector: %s\n", vstr); // "vector: 10, 20, 30"
```
