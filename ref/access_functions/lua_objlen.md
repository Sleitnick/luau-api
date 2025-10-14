---
name: lua_objlen
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

Returns the length of the value at the given stack index. This works for tables (array length), strings (string length), buffers (buffer size), and userdata (userdata size). For non-applicable types, this function will return `0`.

```cpp title="Example" hl_lines="7-10"
lua_pushliteral(L, "hello");
lua_newbuffer(L, 12);
lua_newuserdata(L, 15);
lua_pushinteger(L, 5);

int n;
n = lua_objlen(L, -4); // 5 (length of "hello")
n = lua_objlen(L, -3); // 12 (size of buffer)
n = lua_objlen(L, -2); // 15 (size of userdata)
n = lua_objlen(L, -1); // 0 (integer type is N/A, thus 0 is returned)
```
