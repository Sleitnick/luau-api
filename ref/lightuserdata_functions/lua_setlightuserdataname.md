---
name: lua_setlightuserdataname
ret: void
stack: "-0, +0, -"
args:
  - name: L
    type: lua_State*
    desc: Lua thread
  - name: tag
    type: int
    desc: Tag
  - name: name
    type: const char*
    desc: Name
---

Sets the name for the tagged lightuserdata. The string is copied, so the provided name argument is safe to dispose.

Calling this function more than once for the same tag will throw an error.

```cpp title="Example"
constexpr int kMyDataTag = 10;
lua_setlightuserdataname(L, kMyDataTag, "MyData");
```
