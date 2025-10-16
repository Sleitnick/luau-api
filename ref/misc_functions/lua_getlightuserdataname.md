---
name: lua_getlightuserdataname
ret: const char*
stack: "-0, +0, -"
args:
  - name: L
    type: lua_State*
    desc: Lua thread
  - name: tag
    type: int
    desc: Tag
---

Returns the name for the tagged lightuserdata (or `nullptr` if no name is assigned).

```cpp title="Example" hl_lines="3"
constexpr int kMyDataTag = 10;
lua_setlightuserdataname(L, kMyDataTag, "MyData");
const char* name = lua_getlightuserdataname(L, kMyDataTag); // name == "MyData"
```
