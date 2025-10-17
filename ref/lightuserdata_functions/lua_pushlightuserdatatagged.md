---
name: lua_pushlightuserdatatagged
ret: void
stack: "-0, +1, -"
args:
  - name: L
    type: lua_State*
    desc: Lua thread
  - name: p
    type: void*
    desc: Pointer to arbitrary user-owned data
  - name: tag
    type: int
    desc: Tag
---

Pushes the tagged lightuserdata to the stack. Use [`lua_tolightuserdatatagged`](#lua_tolightuserdatatagged) to retrieve the value. For more info on tags, see the [Tags](guide/tags.md) page.

```cpp title="Example" hl_lines="6"
constexpr int kFooTag = 1;
struct Foo {};

Foo* foo = new Foo();

lua_pushlightuserdatatagged(L, foo, kFooTag);
```
