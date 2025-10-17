---
name: lua_tolightuserdata
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

Returns a pointer to a lightuserdata on the stack. Returns `NULL` if the value is not a lightuserdata.

```cpp title="Example" hl_lines="10"
struct Foo {
	int n;
};

Foo* foo = new Foo();
foo->n = 32;

lua_pushlightuserdata(L, foo);

Foo* f = static_cast<Foo*>(lua_tolightuserdata(L, -1));
printf("foo->n = %d\n", foo->n); // foo->n = 32

// ...pop lightuserdata and delete allocation
```
