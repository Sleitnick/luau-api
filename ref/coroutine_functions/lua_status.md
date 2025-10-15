---
name: lua_status
ret: int
stack: "-0, +0, -"
args:
  - name: L
    type: lua_State*
    desc: Lua thread
---

Returns any `lua_Status` value:
```cpp title="lua_Status"
// Copied from luau/VM/include/lua.h
enum lua_Status {
	  LUA_OK = 0,
    LUA_YIELD,
    LUA_ERRRUN,
    LUA_ERRSYNTAX, // legacy error code, preserved for compatibility
    LUA_ERRMEM,
    LUA_ERRERR,
    LUA_BREAK, // yielded for a debug breakpoint
};
```

```cpp title="Example" hl_lines="15 19 23"
int all_good(lua_State* L) {
	return 0;
}

int oh_no(lua_State* L) {
	luaL_error("oh no!");
}

int yield_something(lua_State* L) {
	return lua_yield(L, 0);
}

lua_State* T = lua_newthread(L);
lua_pushcfunction(all_good, "all_good");
int status = lua_resume(T, nullptr, 0); // LUA_OK (0)

lua_State* T = lua_newthread(L);
lua_pushcfunction(oh_no, "oh_no");
int status = lua_resume(T, nullptr, 0); // LUA_ERRRUN (2)

lua_State* T = lua_newthread(L);
lua_pushcfunction(yield_something, "yield_something");
int status = lua_resume(T, nullptr, 0); // LUA_YIELD (1)
```
