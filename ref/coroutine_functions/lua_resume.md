---
name: lua_resume
ret: int
stack: "-?, +?, -"
args:
  - name: L
    type: lua_State*
    desc: Lua thread
  - name: from
    type: lua_State*
    desc: From Lua thread
  - name: narg
    type: int
    desc: Number of arguments
---

Resumes a coroutine. The status of the resumption is returned.

To start a new coroutine, do the following:
1. Create a new thread, e.g. [`lua_newthread`](#lua_newthread)
1. Place a function onto the new thread's stack
1. Place arguments in-order onto the new thread's stack (same amount as indicated with `narg` argument)
1. Call `lua_resume`
1. Handle the result

To resume an existing coroutine:
1. Place arguments onto the thread's stack (These will be the returned result from Luau's `coroutine.yield` call)
1. Call `lua_resume`
1. Handle the result

```cpp title="Example" hl_lines="22"
int add(lua_State* L) {
	// Get args:
	int a = luaL_checkinteger(L, 1);
	int b = luaL_checkinteger(L, 2);

	lua_pushinteger(L, a + b);

	return 1;
}

// Create thread:
lua_State* T = lua_newthread(L);

// Push function to thread:
lua_pushcfunction(add, "add");

// Push arguments:
lua_pushinteger(T, 10);
lua_pushinteger(T, 20);

// Resume:
int status = lua_resume(T, L, 2);

if (status == LUA_OK) {
	// Coroutine is done
	printf("ok");
} else if (status == LUA_YIELD) {
	// Handle yielded thread
	printf("yielded");
} else {
	// Handle error (call lua_getinfo and lua_debugtrace for better debugging and stacktrace information)
	if (const char* str = lua_tostring(T, -1)) {
		printf("error: %s\n", str);
	} else {
		printf("unknown error: %d\n", status);
	}
}
```
