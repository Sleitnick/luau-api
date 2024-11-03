---
name: lua_typename
ret: const char*
stack: "-0, +0, -"
args:
  - name: L
    type: lua_State*
    desc: Lua thread
  - name: tp
    type: int
    desc: Luau type
---

Returns the name of the given type.

```cpp title="Example"
const char* thread_name = lua_type(L, LUA_TTHREAD);
printf("%s\n", thread_name); // > "thread"
```
