---
name: luaL_sandboxthread
ret: lua_State*
stack: "-0, +0, -"
args:
  - name: L
    type: lua_State*
    desc: Parent thread
---

Sandboxes the given thread by creating a new global table that proxies the original global table.

This is useful to set per "script" rather than every single thread that is created (i.e. it's best to _not_ call `luaL_sandboxthread` within the `userthread` callback, as that can cause long metafield index chains, which will also throw errors at a certain depth).

```cpp title="Example" hl_lines="15"
// Load and run a script:
int run_script(const std::string& name, const std::string& bytecode) {
	int load_res = luau_load(L, (std::string("=") + name).c_str(), bytecode.data(), bytecode.length(), 0);

	if (load_res != 0) {
		// ...handle error
		return load_res;
	}

	lua_State* script = lua_newthread(L);
	lua_pushvalue(L, -2);
	lua_remove(L, -3);
	lua_xmove(L, script, 1);

	lua_sandboxthread(script);

	int status = lua_resume(script, nullptr, 0);
	// ...handle status
}
```
