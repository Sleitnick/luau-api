---
name: lua_pcall
ret: void
stack: "-(nargs + 1), +nresults, -"
args:
  - name: L
    type: lua_State*
    desc: Lua thread
  - name: nargs
    type: int
    desc: Number of arguments
  - name: nresults
    type: int
    desc: Number of returned values
  - name: errfunc
    type: int
    desc: Error function index (or 0 for none)
---

Similar to [`lua_call`](#lua_call), except the function is run in protected mode. The status of the call is returned, which can be checked to see if the call succeeded or not. When successful, results are pushed to the stack in the same way as `lua_call`.

If `errfunc` is set to `0`, then the error message will be put onto the stack. Otherwise, `errfunc` must point to a function on the stack. The function will be called with the given error message. Whatever this error function returns will then be placed onto the stack.

```cpp title="Example" hl_lines="16"
int sub(lua_State* L) {
	double a = luaL_checknumber(L, 1);
	double b = luaL_checknumber(L, 2);
	lua_pushnumber(L, a - b);
	return 1;
}

// First, push the function:
lua_pushcfunction(L, sub, "sub");

// Next, push function arguments in order:
lua_pushnumber(L, 15);
lua_pushnumber(L, 10);

// Finally, call `lua_call`, which will pop the arguments and function from the stack:
int res = lua_pcall(L, 2, 1, 0); // 2 args, 1 result, and no error handler function

if (res == LUA_OK) {
	double difference = lua_tonumber(L, -1); // result is at the top of the stack
	lua_pop(L, 1); // clean up stack

	printf("15 - 10 = %f\n", difference);
} else {
	const char* err = lua_tostring(L, -1);
	lua_pop(L, 1);
	printf("error: %s\n", err);
}
```
