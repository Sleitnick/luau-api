---
name: lua_userdatatag
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

Returns the tag for the userdata at the given stack position. For non-userdata values, this function returns `-1`. If the userdata value was not assigned a tag, the tag will be set to the default of `0`, and thus this function will return `0`.

```cpp title="Example" hl_lines="12-14"
constexpr int kFooTag = 10;
constexpr int kBarTag = 20;

struct Foo {};
struct Bar {};
struct Baz {};

lua_pushuserdatatagged(L, sizeof(Foo), kFooTag);
lua_pushuserdatatagged(L, sizeof(Bar), kBarTag);
lua_pushuserdata(L, sizeof(Baz));

int foo_tag = lua_userdatatag(L, -3); // 10
int bar_tag = lua_userdatatag(L, -2); // 20
int baz_tag = lua_userdatatag(L, -1); // 0
```
