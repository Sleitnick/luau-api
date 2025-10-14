---
name: lua_cpcall
ret: int
stack: "-(nargs + 1), +nresults, -"
args:
  - name: L
    type: lua_State*
    desc: Lua thread
  - name: func
    type: lua_CFunction
    desc: C function
  - name: ud
    type: void*
    desc: Light userdata
---

Calls the C function in protected mode, passing `ud` as the single item on the stack for the function. Returns the status, just like `lua_pcall`. Functions returned by `func` are automatically discarded.

```cpp title="Example" hl_lines="13"
struct Foo {
	int n;
};

int fn(lua_State* L) {
	Foo* foo = static_cast<Foo*>(lua_tolightuserdata(L, 1));
	foo->n *= 2;
	return 0;
}

Foo foo{};
foo.n = 10;
int status = lua_cpcall(L, fn, &foo);

if (status == LUA_OK) {
	printf("n: %d\n", foo.n); // n: 20
} else {
	const char* err = lua_tostring(L, -1);
	lua_pop(L, 1);
	printf("error: %s\n", err);
}
```
