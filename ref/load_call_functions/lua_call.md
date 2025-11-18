---
name: lua_call
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
---

Calls the function at the top of the stack with `nargs` arguments, and expecting `nresults` return values. To use `lua_call`, push the desired function to the stack, and then push the desired arguments to the stack next.

If the function errors, the program will need to handle the error. This differs based on how Luau was built. See [Error Handling](guides/error-handling.md) for more information. Also consider using [`lua_pcall`](#lua_pcall) instead.

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
lua_call(L, 2, 1); // 2 args, 1 result

double difference = lua_tonumber(L, -1); // result is at the top of the stack
lua_pop(L, 1); // clean up stack

printf("15 - 10 = %f\n", difference);
```
