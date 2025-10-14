---
name: lua_pushthread
ret: int
stack: "-0, +1, -"
args:
  - name: L
    type: lua_State*
    desc: Lua thread
---

Pushes the thread (L) to the stack. Returns `1` if the thread is the main thread, otherwise `0`.

```cpp title="Example" hl_lines="1"
lua_pushthread(L);

lua_State* T = lua_tothread(L, -1);
// T == L
```
