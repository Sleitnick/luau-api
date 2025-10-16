---
name: lua_getinfo
ret: int
stack: "-0, +(0|1), -"
args:
  - name: L
    type: lua_State*
    desc: Lua thread
  - name: level
    type: int
    desc: Stack level
  - name: what
    type: const char*
    desc: Desired information
  - name: ar
    type: lua_Debug*
    desc: Debug info (activation record)
---

Gets debug information for the given stack level. The characters in the `what` string indicate what information is desired.

The `what` string may contain:

- `n`: Fills the `name` field
- `s`: Fills the `what`, `source`, `short_src`, and `linedefined` fields
- `l`: Fills the `currentline` field
- `u`: Fills the `nupvals` field
- `a`: Fills the `nparams` and `isvararg` fields
- `f`: Pushes closure to the stack

For example, if `name`, `currentline`, and `short_src` is desired, the `what` string could be set to `"nsl"`.

Returns `0` on failure, otherwise `1`.

```cpp title="Example" hl_lines="10-11"
lua_State* T = lua_newthread(L);
// ... setup T to have a function to resume

int status = lua_resume(T, nullptr, 0);

// Use lua_getinfo to create a clearer error message:
if (status != LUA_OK && status != LUA_YIELD) {
	std::string error;

	lua_Debug ar;
	if (lua_getinfo(L, 0, "nsl")) {
		error += ar.short_src;
		error += ':';
		error += std::to_string(ar.currentline);
		error += ": ";
	}

	if (const char* str = lua_tostring(T, -1)) {
		error += str;
	}

	error += "\nstacktrace:\n";
	error += lua_debugtrace(T);

	fprintf(stderr, "%s\n", error.c_str());
}
```
