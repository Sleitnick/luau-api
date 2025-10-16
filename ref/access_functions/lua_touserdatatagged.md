---
name: lua_touserdatatagged
ret: void*
stack: "-0, +0, -"
args:
  - name: L
    type: lua_State*
    desc: Lua thread
  - name: idx
    type: int
    desc: Stack index
  - name: tag
    type: int
    desc: Tag
---

Returns a pointer to a tagged userdata on the stack. Returns `NULL` if the value is not a userdata _or_ the userdata's tag does not match the provided `tag` argument. For more info on tags, see the [Tags](guide/tags.md) page.

**Note:** It may be unsafe to hang onto a pointer to a userdata value. The Luau GC owns the userdata memory, and may free it. See the page on [pinning](guide/pinning.md) for tips on keeping a value from being GC'd, or consider using [light userdata](guide/light-userdata.md) instead.

```cpp title="Example" hl_lines="10"
constexpr int kFooTag = 1;

struct Foo {
	int n;
};

Foo* foo = static_cast<Foo*>(lua_newuserdatatagged(L, sizeof(Foo), kFooTag));
foo->n = 32;

Foo* f = static_cast<Foo*>(lua_touserdatatagged(L, -1, kFooTag));
printf("foo->n = %d\n", foo->n); // foo->n = 32
```
