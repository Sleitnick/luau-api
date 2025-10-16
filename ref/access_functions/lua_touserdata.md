---
name: lua_touserdata
ret: void*
stack: "-0, +0, -"
args:
  - name: L
    type: lua_State*
    desc: Lua thread
  - name: idx
    type: int
    desc: Stack index
---

Returns a pointer to a userdata on the stack. Returns `NULL` if the value is not a userdata.

If it is preferred to throw an error if the value is not a userdata, use the `luaL_checkuserdata` function instead.

**Note:** It may be unsafe to hang onto a pointer to a userdata value. The Luau GC owns the userdata memory, and may free it. See the page on [pinning](guide/pinning.md) for tips on keeping a value from being GC'd, or consider using [light userdata](guide/light-userdata.md) instead.

```cpp title="Example" hl_lines="8"
struct Foo {
	int n;
};

Foo* foo = static_cast<Foo*>(lua_newuserdata(L, sizeof(Foo)));
foo->n = 32;

Foo* f = static_cast<Foo*>(lua_touserdata(L, -1));
printf("foo->n = %d\n", foo->n); // foo->n = 32
```
