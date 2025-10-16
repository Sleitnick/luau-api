---
name: lua_newuserdata
ret: void*
stack: "-0, +1, -"
args:
  - name: L
    type: lua_State*
    desc: Lua thread
  - name: sz
    type: size_t
    desc: Size of the data
---

Creates a userdata and pushes it to the stack. A pointer to the newly-constructed data is returned. This is equivalent to `lua_newuserdatatagged` with a tag of `0`.

**Note:** Luau-constructed userdata are not zero-initialized. After construction, assign all fields of the object.

```cpp title="Example" hl_lines="5"
struct Foo {
	int n;
};

Foo* foo = static_cast<Foo*>(lua_newuserdata(L, sizeof(Foo)));

// Before explicit assignment, `n` is garbage, so we should initialize it ourselves:
foo->n = 0;
```
