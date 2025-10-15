---
name: lua_resumeerror
ret: int
stack: "-?, +?, -"
args:
  - name: L
    type: lua_State*
    desc: Lua thread
  - name: from
    type: lua_State*
    desc: From Lua thread
---

Resumes a coroutine, but in an error state. This is useful when reporting an error to a yielded thread.

For example, a coroutine might yield to wait for some sort of web request. The yielded thread needs to be resumed, but also needs to report that an error occurred. Thus, `lua_resume` would not be adequate.

The status of the resumption is returned.

```cpp title="Example" hl_lines="8"
// Some sort of error occurs for our thread, e.g. a web request fails
// We'll push a string onto the stack to indicate what went wrong
lua_pushliteral(T, "oh no, the request failed!");

// Elsewhere, in some hypothetical task scheduler, we resume the yielded thread:
int status;
if (there_was_an_error) {
	status = lua_resumeerror(T, L);
} else {
	// ...normal resumption
}

// ...handle status
if (status != LUA_OK && status != LUA_YIELD) {
	const char* err = lua_tostring(T, -1); // Might be our "oh no, the request failed!" error message
	// ...other more complete error handling
}
```
