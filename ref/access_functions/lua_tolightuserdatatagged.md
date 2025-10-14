---
name: lua_tolightuserdatatagged
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

Returns a pointer to a lightuserdata on the stack. Returns `NULL` if the value is not a lightuserdata _or_ if the attached tag does not equal the provided `tag` argument. For more info on tags, see the [Tags](cookbook/tags.md) page.

```cpp title="Example" hl_lines="12"
constexpr int kFooTag = 1;

struct Foo {
	int n;
};

Foo* foo = new Foo();
foo->n = 32;

lua_pushlightuserdatatagged(L, foo, kFooTag);

Foo* f = static_cast<Foo*>(lua_tolightuserdatatagged(L, -1, kFooTag));
printf("foo->n = %d\n", foo->n); // foo->n = 32

// ...pop lightuserdata and delete allocation
```
