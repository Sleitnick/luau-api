---
name: lua_yield
ret: void
stack: "-?, +?, -"
args:
  - name: L
    type: lua_State*
    desc: Lua thread
  - name: nresults
    type: int
    desc: Number of returned values
---

Yields a coroutine thread. This should only be called as the return value of a C function.

The `nresults` argument indicates how many stack values remain on the thread's stack, allowing the caller of `lua_resume` to grab those values.

```cpp title="Example"
int do_something(lua_State* L) {
	// Yield back '15' to the lua_resume call:
	lua_pushinteger(L, 15);
	return lua_yield(L, 1);
}

lua_State* T = lua_newthread(L);
lua_pushcfunction(T, do_something, "do_something");
int status = lua_resume(L, 0);
if (status == LUA_YIELD) {
  int value = lua_tointeger(T, 1); // 15
  lua_pop(T, 1);
}
```
