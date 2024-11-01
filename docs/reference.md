# Luau C API Reference

## State Manipulation

### <span class="subsection">`lua_newstate`</span>

<span class="signature">`lua_State* lua_newstate(lua_Alloc f, void* ud)`</span>
<span class="stack">`[-0, +0, -]`</span>

- `f`: Luau allocator function.
- `ud`: Opaque userdata pointer that is passed to the allocator function.


Creates a new Luau state. If the allocator fails to allocate
memory for the new state, this function will return `nullptr`.
Use `lua_close()` to close the state once done.

The allocator function is used for all Luau memory allocations, including the initial construction of the state itself.

```cpp hl_lines="1"
lua_State* L = lua_newstate(allocator, nullptr);
lua_close(L);
```

??? note "Allocator Example"
	This is functionally identical to the allocator function used by the `luaL_newstate` helper function.
	```cpp
	static void* allocator(void* ud, void* ptr, size_t old_size, size_t new_size) {
		(void)ud; (void)old_size; // Not using these

		// new_size of 0 indicates the allocator should free the ptr
		if (new_size == 0) {
			free(ptr);
			return nullptr;
		}

		return realloc(ptr, new_size);
	}

	lua_State* L = lua_newstate(allocator, nullptr);
	```


----


### <span class="subsection">`luaL_newstate`</span>

<span class="signature">`lua_State* luaL_newstate()`</span>
<span class="stack">`[-0, +0, -]`</span>


A simplified version of `lua_newstate` that uses the default allocator, which uses the standard `free` and `realloc` memory functions.


----


### <span class="subsection">`lua_close`</span>

<span class="signature">`void lua_close()`</span>
<span class="stack">`[-0, +0, -]`</span>

Closes the Luau state. Luau objects are garbage collected and any dynamic memory is freed.

??? note "Smart Pointer Example"
	In modern C++, smart pointers can help with memory management. Here is an example of
	using a smart pointer that wraps around a Luau state and automatically calls `lua_close()`
	when dereferenced.
	``` cpp
	std::unique_ptr<lua_State, void(*)(lua_State*)> state(luaL_newState(), lua_close);
	```


----


### <span class="subsection">`lua_newthread`</span>

<span class="signature">`lua_State* lua_newthread(lua_State* L)`</span>
<span class="stack">`[-0, +1, -]`</span>

- `L`: Parent thread


Creates a new Luau thread.


----


### <span class="subsection">`lua_mainthread`</span>

<span class="signature">`lua_State* lua_mainthread(lua_State* L)`</span>
<span class="stack">`[-0, +0, -]`</span>

- `L`: Lua thread


Returns the main Lua state (e.g. the state created from `lua_newstate()`).


----


### <span class="subsection">`lua_resetthread`</span>

<span class="signature">`void lua_resetthread(lua_State* L)`</span>
<span class="stack">`[-0, +0, -]`</span>

- `L`: Lua thread


Resets the Lua thread.


----


### <span class="subsection">`lua_isthreadreset`</span>

<span class="signature">`int lua_isthreadreset(lua_State* L)`</span>
<span class="stack">`[-0, +0, -]`</span>

- `L`: Lua thread


Checks if the Lua thread is reset.


## Basic Stack Manipulation

### <span class="subsection">`lua_absindex`</span>

<span class="signature">`int lua_absindex(lua_State* L, int idx)`</span>
<span class="stack">`[-0, +0, -]`</span>

- `L`: Lua thread
- `idx`: Index


Gets the absolute stack index. For example, if `idx` is `-2`, and the stack has 5 items, this function will return `4`.


----


### <span class="subsection">`lua_gettop`</span>

<span class="signature">`int lua_gettop(lua_State* L)`</span>
<span class="stack">`[-0, +0, -]`</span>

- `L`: Lua thread


Gets the index representing the top of the stack. This also represents the number of items on the stack, since the stack index starts at 1. A stack size of 0 indicates an empty stack.

A common use of `lua_gettop()` is to get the number of arguments in a function call.

```cpp
int custom_fn(lua_State* L) {
	int n_args = lua_gettop(L);
	lua_pushfstring("there are %d arguments", n_args);
	return 1;
}
```


----


### <span class="subsection">`lua_settop`</span>

<span class="signature">`int lua_settop(lua_State* L, int idx)`</span>
<span class="stack">`[-?, +?, -]`</span>

- `L`: Lua thread
- `idx`: Top stack index


Sets the top of the stack, essentially resizing it to the given index. If the new size is larger than the current size, the new elements in the stack will be filled with `nil` values. Setting the stack size to 0 will clear the stack entirely.

```cpp
lua_settop(L, 0); // clear the stack
```


----


### <span class="subsection">`lua_pushvalue`</span>

<span class="signature">`void lua_pushvalue(lua_State* L, int idx)`</span>
<span class="stack">`[-0, +1, -]`</span>

- `L`: Lua thread
- `idx`: Stack index


TODO


----


### <span class="subsection">`lua_remove`</span>

<span class="signature">`void lua_remove(lua_State* L, int idx)`</span>
<span class="stack">`[-1, +0, -]`</span>

- `L`: Lua thread
- `idx`: Stack index


TODO


----


### <span class="subsection">`lua_insert`</span>

<span class="signature">`void lua_insert(lua_State* L, int idx)`</span>
<span class="stack">`[-0, +1, -]`</span>

- `L`: Lua thread
- `idx`: Stack index


TODO


----


### <span class="subsection">`lua_replace`</span>

<span class="signature">`void lua_replace(lua_State* L, int idx)`</span>
<span class="stack">`[-1, +0, -]`</span>

- `L`: Lua thread
- `idx`: Stack index


TODO


----


### <span class="subsection">`lua_checkstack`</span>

<span class="signature">`int lua_checkstack(lua_State* L, int size)`</span>
<span class="stack">`[-0, +0, m]`</span>

- `L`: Lua thread
- `size`: Desired stack size


TODO


----


### <span class="subsection">`lua_rawcheckstack`</span>

<span class="signature">`void lua_rawcheckstack(lua_State* L, int size)`</span>
<span class="stack">`[-0, +0, m]`</span>

- `L`: Lua thread
- `size`: Desired stack size


TODO
