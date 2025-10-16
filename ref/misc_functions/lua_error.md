---
name: lua_error
ret: l_noret
stack: "-0, +0, -"
args:
  - name: L
    type: lua_State*
    desc: Lua thread
---

Throws a Luau error. Expects the error message to be on the top of the stack. Depending on how Luau is built, this will either perform a `longjmp` or throw a C++ `luau_exception`. See [Error Handling](guide/error-handling.md) for more information.

Using [`luaL_error`](#luaL_error) is typically a more ergonomic way to throw errors, since an error message can be provided.

```cpp title="Example"
int multiply_by_two(lua_State* L) {
	// This is just for example (could use luaL_checknumber instead)
	if (lua_type(L, 1) != LUA_TNUMBER) {
		// 1. Push error message to the stack:
		lua_pushfstring(L, "expected number; got %s", luaL_typename(L, 1));
		// 2. Throw error
		lua_error(L);
	}

	double n = lua_tonumber(L, 1);
	lua_pushnumber(L, n * 2.0);
	return 1;
}
// ...
lua_pushcfunction(multiply_by_two, "multiply_by_two");
lua_setglobal(L, "multiply_by_two");
```

```luau title="Luau Example"
-- throws error: "expected number; got string"
multiply_by_two("abc")
```
