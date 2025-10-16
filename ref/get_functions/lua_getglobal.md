---
name: lua_getglobal
ret: int
stack: "-0, +1, -"
args:
  - name: L
    type: lua_State*
    desc: Lua thread
  - name: k
    type: const char*
    desc: Field
---

Pushes a value from the global table onto the stack. Use [`lua_setglobal`](#lua_setglobal) to set a new global value.

Returns the type of the value.

```cpp title="Example" hl_lines="4"
lua_pushliteral(L, "hello");
lua_setglobal(L, "message"); // _G.message = "hello"

lua_getglobal(L, "message");
const char* s = lua_tostring(L, -1); // s == "hello"
```
