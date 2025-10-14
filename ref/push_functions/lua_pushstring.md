---
name: lua_pushstring
ret: void
stack: "-0, +1, -"
args:
  - name: L
    type: lua_State*
    desc: Lua thread
  - name: str
    type: const char*
    desc: C-style string
---

Pushes string `str` to the stack. The length of the string is determined internally using the C `strlen` function.

If the length of the string is known, it is more efficient to use [`lua_pushlstring`](#lua_pushlstring).

Internally, strings in Luau are copied and interned. Thus, modifications made to the inputted string will not be reflected in the Luau string value.

```cpp title="Example"
const char* str = "hello";
lua_pushstring(L, str);
```
