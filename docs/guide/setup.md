# Setup

## New Instance

To create a new instance, call either `lua_newstate` or `luaL_newstate`. The former allows you to assign your own allocator, along with an opaque pointer to arbitrary data. The latter will use a default allocator.

The default allocator looks like this:
```cpp title="Allocator"
static void* allocator(void* ud, void* ptr, size_t old_size, size_t new_size) {
	// 'ud' is the pointer passed as the second argument to `lua_newstate`

	(void)ud; (void)old_size; // Not using these

	// new_size of 0 signals that the allocator should free the memory
	if (new_size == 0) {
		free(ptr);
		return nullptr;
	}

	return realloc(ptr, new_size);
}
```

```cpp title="New State"
// Create a Luau state with a specified allocator:
lua_State* L = lua_newstate(allocator, nullptr);

// Use the default allocator:
lua_State* L = luaL_newstate();
```

## Libraries

Once our Luau state is open, we need to load the default libraries. The easiest way to do this is by calling `luaL_openlibs(L)`, which opens up all of the built-in libraries. Alternatively, if opening all of the libraries is not desired, individual built-in ones can be opened using their respective open function, e.g. `luaopen_os(L)`.

You may also have your own custom libraries. Open these right after opening the built-in libraries.

```cpp title="Libraries" hl_lines="3"
lua_State* L = luaL_newstate();

luaL_openlibs(L);
```

## Sandboxing

Sandboxing creates a safer environment for potentially untrusted Luau code. To turn on sandboxing, call `luaL_sandbox(L)` _after_ opening up libraries and _before_ loading any Luau code.

```cpp title="Sandboxing" hl_lines="4"
lua_State* L = luaL_newstate();
luaL_openlibs(L);

luaL_sandbox(L);
```

See the [Sandboxing](sandboxing.md) guide for more information.

## Closing

States need to be closed once completed with them.

```cpp title="Closing"
lua_close(L);
```

## Smart Pointer

We can utilize smart pointers to automatically clean up the state once out of scope.

```cpp
std::unique_ptr<lua_State, void(*)(lua_State*)> state(luaL_newState(), lua_close);
```
