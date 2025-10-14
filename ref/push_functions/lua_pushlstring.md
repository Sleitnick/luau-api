---
name: lua_pushlstring
ret: void
stack: "-0, +1, -"
args:
  - name: L
    type: lua_State*
    desc: Lua thread
  - name: str
    type: const char*
    desc: C-style string
  - name: len
    type: size_t
    desc: String length
---

Pushes string `str` to the stack with a length of `len`.

Internally, strings in Luau are copied and interned. Thus, modifications made to the inputted string will not be reflected in the Luau string value.

This function is preferred over [`lua_pushstring`](#lua_pushstring) if the string length is known, or if the string contains `\0` characters as part of the string itself.

```cpp title="Example"
std::string str = "hello";
lua_pushlstring(L, str.c_str(), str.size());
```
