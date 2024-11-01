---
name: lua_close
ret: void
stack: "-0, +0, -"
args:
---
Closes the Luau state. Luau objects are garbage collected and any dynamic memory is freed.

??? note "Example"
	``` cpp
	lua_close(L);
	```

??? note "Smart Pointer"
	``` cpp
	std::unique_ptr<lua_State, void(*)(lua_State*)> state(luaL_newState(), lua_close);
	```
