---
name: lua_lightuserdatatag
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

Returns the tag for the lightuserdata at the given stack position. For non-lightuserdata values, this function returns `-1`. If the lightuserdata value was not assigned a tag, the tag will be set to the default of `0`, and thus this function will return `0`.

```cpp title="Example" hl_lines="17-19"
constexpr int kFooTag = 10;
constexpr int kBarTag = 20;

struct Foo {};
struct Bar {};
struct Baz {};

Foo* foo = new Foo();
lua_pushlightuserdatatagged(L, foo, kFooTag);

Bar* bar = new Bar();
lua_pushlightuserdatatagged(L, bar, kBarTag);

Baz* baz = new Baz();
lua_pushlightuserdata(L, baz);

int foo_tag = lua_lightuserdatatag(L, -3); // 10
int bar_tag = lua_lightuserdatatag(L, -2); // 20
int baz_tag = lua_lightuserdatatag(L, -1); // 0

// ...pop lightuserdata and delete allocations
```
