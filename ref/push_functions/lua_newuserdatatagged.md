---
name: lua_newuserdatatagged
ret: void*
stack: "-0, +1, -"
args:
  - name: L
    type: lua_State*
    desc: Lua thread
  - name: sz
    type: size_t
    desc: Size of the data
  - name: tag
    type: int
    desc: Tag
---

Creates the tagged userdata and pushes it to the stack. A pointer to the newly-constructed data is returned. Use [`lua_touserdatatagged`](lua_touserdatatagged) to retrieve the value. For more info on tags, see the [Tags](guide/tags.md) page.

**Note:** Luau-constructed userdata are not zero-initialized. After construction, assign all fields of the object.

```cpp title="Example" hl_lines="6"
constexpr int kFooTag = 1;
struct Foo {
	int n;
};

Foo* foo = static_cast<Foo*>(lua_newuserdatatagged(L, sizeof(Foo), kFooTag));

// Before explicit assignment, `n` is garbage, so we should initialize it ourselves:
foo->n = 0;
```
