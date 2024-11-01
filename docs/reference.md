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


Pushes a copy of the value at index `idx` to the top of the stack.


----


### <span class="subsection">`lua_remove`</span>

<span class="signature">`void lua_remove(lua_State* L, int idx)`</span>
<span class="stack">`[-1, +0, -]`</span>

- `L`: Lua thread
- `idx`: Stack index


Removes the value at the given stack index `idx`. All other values above the index are shifted down.

```cpp title="Example" hl_lines="5"
lua_pushinteger(L, 10);
lua_pushboolean(L, true);
lua_pushliteral(L, "hello");

lua_remove(L, -2); // remove the 'true' value.

printf("%s\n", luaL_tostring(L, -2)); // 'hello'
```


----


### <span class="subsection">`lua_insert`</span>

<span class="signature">`void lua_insert(lua_State* L, int idx)`</span>
<span class="stack">`[-1, +1, -]`</span>

- `L`: Lua thread
- `idx`: Stack index


Moves the top stack element into the given index, shifting other values up first to give space. The element right under the top stack element becomes the new top element.

```cpp title="Example" hl_lines="15"
lua_pushboolean(L, true);
lua_pushinteger(L, 10);
lua_pushliteral(L, "hello");
lua_pushinteger(L, 20);

// Current stack order:
// [-4] true
// [-3] 10
// [-2] hello
// [-1] 20

// Move the top value (20) to index -3.
// The values below the top and above -3 are shifted up.
// e.g. the '10' and 'hello' are shifted up first.
lua_insert(L, -3);

// New stack order:
// [-4] true
// [-3] 20
// [-2] 10
// [-1] hello
```


----


### <span class="subsection">`lua_replace`</span>

<span class="signature">`void lua_replace(lua_State* L, int idx)`</span>
<span class="stack">`[-1, +0, -]`</span>

- `L`: Lua thread
- `idx`: Stack index


Moves the top element over top of the `idx` stack index. The old value at `idx` is overwritten. The top element is popped.

```cpp title="Example" hl_lines="15"
lua_pushboolean(L, true);
lua_pushinteger(L, 10);
lua_pushliteral(L, "hello");
lua_pushinteger(L, 20);

// Current stack order:
// [-4] true
// [-3] 10
// [-2] hello
// [-1] 20

// Move the top value (20) to index -3.
// The values below the top and above -3 are shifted up.
// e.g. the '10' and 'hello' are shifted up first.
lua_replace(L, -3);

// New stack order:
// [-3] true
// [-2] 20
// [-1] hello
```


----


### <span class="subsection">`lua_checkstack`</span>

<span class="signature">`int lua_checkstack(lua_State* L, int size)`</span>
<span class="stack">`[-0, +0, m]`</span>

- `L`: Lua thread
- `size`: Desired stack size


Ensures the stack is large enough to hold `size` _more_ elements. This will only grow the stack, not shrink it. Returns true if successful, or false if it fails (e.g. the max stack size exceeded).

```cpp title="Example" hl_lines="2"
// Ensure there are at least 2 more slots on the stack:
if (lua_checkstack(L, 2)) {
	lua_pushinteger(L, 10);
	lua_pushinteger(L, 20);
}
```


----


### <span class="subsection">`lua_rawcheckstack`</span>

<span class="signature">`void lua_rawcheckstack(lua_State* L, int size)`</span>
<span class="stack">`[-0, +0, m]`</span>

- `L`: Lua thread
- `size`: Desired stack size


Similar to `lua_checkstack`, except it bypasses the max stack limit.


----


### <span class="subsection">`lua_xmove`</span>

<span class="signature">`void lua_xmove(lua_State* from, lua_State* to, int n)`</span>
<span class="stack">`[-?, +?, -]`</span>

- `from`: Lua thread
- `to`: Lua thread
- `n`: Number of items to move


Moves the top `n` elements in the `from` stack to the top of the `to` stack. This pops `n` values from the `from` stack and pushes `n` values to the `to` stack.

Note: Both `from` and `to` states must share the same global state (e.g. the main state created with `lua_newstate`).

```cpp title="Example" hl_lines="9"
// Assume we have lua_State* A and B, both starting with empty stacks.

// Add some items to 'A' stack:
lua_pushboolean(A, true);
lua_pushinteger(A, 10);
lua_pushliteral(A, "hello");

// Moves the top 2 values from 'A' to 'B' (e.g. '10' and 'hello')
lua_xmove(A, B, 2);

printf("%d\n", lua_gettop(A)); // 1 (just the 'true' value remains)
printf("%d\n", lua_gettop(B)); // 2 (the '10' and 'hello' values)
```


----


### <span class="subsection">`lua_xpush`</span>

<span class="signature">`void lua_xpush(lua_State* from, lua_State* to, int idx)`</span>
<span class="stack">`[-0, +1, -]`</span>

- `from`: Lua thread
- `to`: Lua thread
- `idx`: Stack index


Pushes a value from the `from` state to the `to` state. The value at index `idx` in `from` is pushed to the top of the `to` stack. This is similar to `lua_pushvalue`, except the value is pushed to a different state.

Similar to `lua_xmove`, both `from` and `to` must share the same global state.

```cpp title="Example"
// Push the value at index -2 within 'from' to the top of the 'to' stack:
lua_xpush(from, to, -2);
```
