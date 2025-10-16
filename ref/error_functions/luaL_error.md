---
name: luaL_error
ret: l_noret
stack: "-0, +0, -"
args:
  - name: L
    type: lua_State*
    desc: Lua thread
  - name: fmt
    type: const char*
    desc: Format string
  - name: ...
    type: ""
    desc: Args
---

Throws a Luau error with the given error message.

```cpp title="Example"
luaL_error(L, "something went wrong");

// Error message can be formatted:
int some_code = 2;
const char* message = "it zigged but it should have zagged";
luaL_error(L, "%d - %s", some_code, message);
```
