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


----


### <span class="subsection">`luaL_sandbox`</span>

<span class="signature">`lua_State* luaL_sandbox(lua_State* L)`</span>
<span class="stack">`[-0, +0, -]`</span>

- `L`: Parent thread


Sandboxes the Luau state. All libraries, built-in metatables, and globals are set to read-only. This also activates "safeenv" (`lua_setsafeenv`) on the global table.

```cpp title="Example"
lua_State* L = luaL_newstate();
luaL_openlibs(L);

// Sandboxing AFTER libraries are open:
luaL_sandbox(L);
```


----


### <span class="subsection">`luaL_sandboxthread`</span>

<span class="signature">`lua_State* luaL_sandboxthread(lua_State* L)`</span>
<span class="stack">`[-0, +0, -]`</span>

- `L`: Parent thread


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


----


## Open Library Functions

### <span class="subsection">`luaL_openlibs`</span>

<span class="signature">`int luaL_openlibs(lua_State* L)`</span>
<span class="stack">`[-0, +0, -]`</span>

- `L`: Lua thread


Opens all built-in Luau libraries.

```cpp title="Example"
lua_State* L = luaL_newstate();
luaL_openlibs(L);
// ...
```


----


### <span class="subsection">`luaopen_base`</span>

<span class="signature">`int luaopen_base(lua_State* L)`</span>
<span class="stack">`[-0, +1, -]`</span>

- `L`: Lua thread


Opens the base global library functions, e.g. `print`, `error`, `tostring`, etc.

Use [`luaL_openlibs`](#lual_openlibs) to open all built-in Luau libraries, including this one.


----


### <span class="subsection">`luaopen_coroutine`</span>

<span class="signature">`int luaopen_coroutine(lua_State* L)`</span>
<span class="stack">`[-0, +1, -]`</span>

- `L`: Lua thread


Opens the coroutine library. Use [`luaL_openlibs`](#lual_openlibs) to open all built-in Luau libraries, including this one.


----


### <span class="subsection">`luaopen_table`</span>

<span class="signature">`int luaopen_table(lua_State* L)`</span>
<span class="stack">`[-0, +1, -]`</span>

- `L`: Lua thread


Opens the table library. Use [`luaL_openlibs`](#lual_openlibs) to open all built-in Luau libraries, including this one.


----


### <span class="subsection">`luaopen_os`</span>

<span class="signature">`int luaopen_os(lua_State* L)`</span>
<span class="stack">`[-0, +1, -]`</span>

- `L`: Lua thread


Opens the OS library. Use [`luaL_openlibs`](#lual_openlibs) to open all built-in Luau libraries, including this one.


----


### <span class="subsection">`luaopen_string`</span>

<span class="signature">`int luaopen_string(lua_State* L)`</span>
<span class="stack">`[-0, +1, -]`</span>

- `L`: Lua thread


Opens the string library. Use [`luaL_openlibs`](#lual_openlibs) to open all built-in Luau libraries, including this one.


----


### <span class="subsection">`luaopen_bit32`</span>

<span class="signature">`int luaopen_bit32(lua_State* L)`</span>
<span class="stack">`[-0, +1, -]`</span>

- `L`: Lua thread


Opens the bit32 library. Use [`luaL_openlibs`](#lual_openlibs) to open all built-in Luau libraries, including this one.


----


### <span class="subsection">`luaopen_buffer`</span>

<span class="signature">`int luaopen_buffer(lua_State* L)`</span>
<span class="stack">`[-0, +1, -]`</span>

- `L`: Lua thread


Opens the buffer library. Use [`luaL_openlibs`](#lual_openlibs) to open all built-in Luau libraries, including this one.


----


### <span class="subsection">`luaopen_utf8`</span>

<span class="signature">`int luaopen_utf8(lua_State* L)`</span>
<span class="stack">`[-0, +1, -]`</span>

- `L`: Lua thread


Opens the UTF-8 library. Use [`luaL_openlibs`](#lual_openlibs) to open all built-in Luau libraries, including this one.


----


### <span class="subsection">`luaopen_math`</span>

<span class="signature">`int luaopen_math(lua_State* L)`</span>
<span class="stack">`[-0, +1, -]`</span>

- `L`: Lua thread


Opens the math library. Use [`luaL_openlibs`](#lual_openlibs) to open all built-in Luau libraries, including this one.


----


### <span class="subsection">`luaopen_debug`</span>

<span class="signature">`int luaopen_debug(lua_State* L)`</span>
<span class="stack">`[-0, +1, -]`</span>

- `L`: Lua thread


Opens the debug library. Use [`luaL_openlibs`](#lual_openlibs) to open all built-in Luau libraries, including this one.


----


### <span class="subsection">`luaopen_vector`</span>

<span class="signature">`int luaopen_vector(lua_State* L)`</span>
<span class="stack">`[-0, +1, -]`</span>

- `L`: Lua thread


Opens the vector library. Use [`luaL_openlibs`](#lual_openlibs) to open all built-in Luau libraries, including this one.


----


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


### <span class="subsection">`lua_pop`</span>

<span class="signature">`void lua_pop(lua_State* L, int n)`</span>
<span class="stack">`[-n, +0, -]`</span>

- `L`: Lua thread
- `n`: Number of items to pop


Pops `n` values off the top of the stack.

```cpp title="Example" hl_lines="8"
// Assume lua_gettop(L) == 0 here

lua_pushliteral(L, "Hello");
lua_pushnumber(L, 85.2);
lua_pushboolean(L, true);
printf("Size: %d\n", lua_gettop(L)); // Size: 3

lua_pop(L, 2);

printf("Size: %d\n", lua_gettop(L)); // Size: 1
printf("Type: %s\n", luaL_typename(L, -1)); // string (top of stack is the "Hello" value now)
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


### <span class="subsection">`lua_checkstack`</span>

<span class="signature">`void lua_checkstack(lua_State* L, int size, const char* msg)`</span>
<span class="stack">`[-0, +0, m]`</span>

- `L`: Lua thread
- `size`: Desired stack size
- `msg`: Error message


Ensures the stack is large enough to hold `size` _more_ elements. This will only grow the stack, not shrink it. Throws an error if the stack cannot be resized to the desired size.

```cpp title="Example"
// Ensure there are at least 2 more slots on the stack:
luaL_checkstack(L, 2, "failed to grow stack for the two numbers");

lua_pushinteger(L, 10);
lua_pushinteger(L, 20);
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


----


## Access Functions

### <span class="subsection">`lua_iscfunction`</span>

<span class="signature">`int lua_iscfunction(lua_State* L, int idx)`</span>
<span class="stack">`[-0, +0, -]`</span>

- `L`: Lua thread
- `idx`: Stack index


Returns `1` if the value at the given stack index is a C function. Otherwise, returns `0`.


----


### <span class="subsection">`lua_isLfunction`</span>

<span class="signature">`int lua_isLfunction(lua_State* L, int idx)`</span>
<span class="stack">`[-0, +0, -]`</span>

- `L`: Lua thread
- `idx`: Stack index


Returns `1` if the value at the given stack index is a Luau function. Otherwise, returns `0`.


----


### <span class="subsection">`lua_type`</span>

<span class="signature">`int lua_type(lua_State* L, int idx)`</span>
<span class="stack">`[-0, +0, -]`</span>

- `L`: Lua thread
- `idx`: Stack index


Returns the value type at the given stack index. If the stack index is invalid, this function returns `LUA_TNONE`.

List of lua types:

- `LUA_TNIL`
- `LUA_TBOOLEAN`
- `LUA_TLIGHTUSERDATA`
- `LUA_TNUMBER`
- `LUA_TVECTOR`
- `LUA_TSTRING`
- `LUA_TTABLE`
- `LUA_TFUNCTION`
- `LUA_TUSERDATA`
- `LUA_TTHREAD`
- `LUA_TBUFFER`


----


### <span class="subsection">`lua_typename`</span>

<span class="signature">`const char* lua_typename(lua_State* L, int tp)`</span>
<span class="stack">`[-0, +0, -]`</span>

- `L`: Lua thread
- `tp`: Luau type


Returns the name of the given type.

```cpp title="Example"
const char* thread_name = lua_type(L, LUA_TTHREAD);
printf("%s\n", thread_name); // > "thread"
```


----


### <span class="subsection">`lua_equal`</span>

<span class="signature">`int lua_equal(lua_State* L, int idx1, int idx2)`</span>
<span class="stack">`[-0, +0, -]`</span>

- `L`: Lua thread
- `idx1`: Stack index
- `idx2`: Stack index


Returns `1` if the values at `idx1` and `idx2` are equal. If applicable, this will call the `__eq` metatable function. Use `lua_rawequal` to avoid the metatable call. Returns `0` if the values are not equal (including if either of the indices are invalid).

```cpp title="Example" hl_lines="4"
lua_pushliteral(L, "hello");
lua_pushliteral(L, "hello");

if (lua_equal(L, -2, -1)) {
	printf("equal\n");
}
```


----


### <span class="subsection">`lua_rawequal`</span>

<span class="signature">`int lua_rawequal(lua_State* L, int idx1, int idx2)`</span>
<span class="stack">`[-0, +0, -]`</span>

- `L`: Lua thread
- `idx1`: Stack index
- `idx2`: Stack index


The same as `lua_equal`, except it does not call any metatable `__eq` functions.


----


### <span class="subsection">`lua_lessthan`</span>

<span class="signature">`int lua_lessthan(lua_State* L, int idx1, int idx2)`</span>
<span class="stack">`[-0, +0, -]`</span>

- `L`: Lua thread
- `idx1`: Stack index
- `idx2`: Stack index


Returns `1` if the value at `idx` is less than the value at `idx2`. Otherwise, returns `0`. This may call the `__lt` metamethod function. Also returns `0` if either index is invalid.


----


### <span class="subsection">`lua_namecallatom`</span>

<span class="signature">`const char* lua_namecallatom(lua_State* L, int* atom)`</span>
<span class="stack">`[-0, +0, -]`</span>

- `L`: Lua thread
- `atom`: Atom


When called within a `__namecall` metamethod, this function returns the name of the called method. An optional atom value can be utilized as well.

```cpp title="Example" hl_lines="6-14"
static constexpr const char* kFoo = "Foo";

struct Foo {};

// Handle namecalls, e.g. Luau calling "foo:Hello()"
static int Foo_namecall(lua_State* L) {
	const char* method = lua_namecallatom(L, nullptr);
	if (strcmp(method, "Hello") == 0) {
		// User called the 'Hello' method. Return "Goodbye":
		lua_pushliteral(L, "Goodbye");
		return 1;
	}
	luaL_error(L, "unknown method %s", method);
}

// Construct new Foo userdata:
int new_Foo(lua_State* L) {
	Foo* foo = static_cast<Foo*>(lua_newuserdata(L, sizeof(Foo)));
	if (luaL_newmetatable(L, kFoo)) {
		// Assign __namecall metamethod:
		lua_pushcfunction(L, Foo_namecall, "namecall");
		lua_rawsetfield(L, "__namecall", -2);
	}
	lua_setmetatable(L, -2);
	return 1;
}

static const luaL_Reg[] Foo_lib = {
	{"new", new_Foo},
	{nullptr, nullptr},
};

// Called from setup code for Luau state:
void open_Foo(lua_State* L) {
	lua_register(L, Foo_lib);
}
```


----


### <span class="subsection">`lua_objlen`</span>

<span class="signature">`int lua_objlen(lua_State* L, int idx)`</span>
<span class="stack">`[-0, +0, -]`</span>

- `L`: Lua thread
- `idx`: Stack index


Returns the length of the value at the given stack index. This works for tables (array length), strings (string length), buffers (buffer size), and userdata (userdata size). For non-applicable types, this function will return `0`.

```cpp title="Example" hl_lines="7-10"
lua_pushliteral(L, "hello");
lua_newbuffer(L, 12);
lua_newuserdata(L, 15);
lua_pushinteger(L, 5);

int n;
n = lua_objlen(L, -4); // 5 (length of "hello")
n = lua_objlen(L, -3); // 12 (size of buffer)
n = lua_objlen(L, -2); // 15 (size of userdata)
n = lua_objlen(L, -1); // 0 (integer type is N/A, thus 0 is returned)
```


----


### <span class="subsection">`lua_tocfunction`</span>

<span class="signature">`lua_CFunction lua_tocfunction(lua_State* L, int idx)`</span>
<span class="stack">`[-0, +0, -]`</span>

- `L`: Lua thread
- `idx`: Stack index


Returns the C function at the given stack position. If the value is not a C function, this function returns `NULL`.

```cpp title="Example" hl_lines="6"
int hello() {
  printf("hello\n");
  return 0;
}

lua_pushcfunction(L, hello, "hello");

lua_CFunction f = lua_tocfunction(L, -1);
if (f) {
  f(); // hello
}
```


----


### <span class="subsection">`lua_tothread`</span>

<span class="signature">`lua_State* lua_tothread(lua_State* L, int idx)`</span>
<span class="stack">`[-0, +0, -]`</span>

- `L`: Lua thread
- `idx`: Stack index


Returns the Luau thread at the given stack index, or `NULL` if the value is not a Luau thread.

```cpp title="Example" hl_lines="2"
lua_State* T = lua_newthread(L); // pushes T onto L's stack
lua_State* thread = lua_tothread(L, -1); // retrieve T from L's stack
// thread == T
```


----


### <span class="subsection">`lua_topointer`</span>

<span class="signature">`void* lua_topointer(lua_State* L, int idx)`</span>
<span class="stack">`[-0, +0, -]`</span>

- `L`: Lua thread
- `idx`: Stack index


Returns a pointer to the value at the given stack index. This works for userdata, lightuserdata, strings, tables, buffers, and functions.

**Note:** This should only be used for debugging purposes.

```cpp title="Example" hl_lines="4"
void* buf = lua_newbuffer(L, 10);

size_t len;
void* b = lua_tobuffer(L, -1, &len);
// b == buf
// len == 10
```


----


## Push Functions

### <span class="subsection">`lua_pushnil`</span>

<span class="signature">`void lua_pushnil(lua_State* L)`</span>
<span class="stack">`[-0, +1, -]`</span>

- `L`: Lua thread


Pushes `nil` to the Luau stack.

```cpp title="Example"
lua_pushnil(L);
```


----


### <span class="subsection">`lua_pushcclosurek`</span>

<span class="signature">`void lua_pushcclosurek(lua_State* L, lua_CFunction fn, const char* debugname, int nup, lua_Continuation cont)`</span>
<span class="stack">`[-n, +1, -]`</span>

- `L`: Lua thread
- `fn`: C Function
- `debugname`: Debug name
- `nup`: Number of upvalues to capture
- `cont`: Continuation function to invoke


Pushes the C function to the stack as a closure, which captures and pops `nup` upvalues from the top of the stack. The closure's continuation function is also assigned to `cont`.

The continuation function is invoked when the closure is resumed.

```cpp title="Example" hl_lines="23"
int addition_cont(lua_State* L) {
	double add = lua_tonumber(L, lua_upvalueindex(2)); // 4
	double n = lua_tonumber(L, 1);
	double sum = n + add;
	lua_pushnumber(L, sum);
	// Stop generator if sum exceeds 100 (this would obviously be bad if 'add' was <= 0)
	if (sum > 100) {
		return 1;
	}
	return lua_yield(L, 1);
}

int addition(lua_State* L) {
	double start = lua_tonumber(L, lua_upvalueindex(1)); // 10
	double add = lua_tonumber(L, lua_upvalueindex(2)); // 4
	lua_pushnumber(L, start + add);
	return lua_yield(L, 1);
}

int start_addition(lua_State* L) {
	lua_pushvalue(L, 1);
	lua_pushvalue(L, 2);
	lua_pushcclosurek(L, addition, "addition", 2, addition_cont);
}

// Expose "start_addition" to Luau:
set_global(L, "start_addition", start_addition);
```

```lua
-- Start adder generator from 10 and add by 4:
local adder = coroutine.wrap(start_addition(10, 4))
do
	local sum = adder()
	print(sum)
until not sum
```


----


### <span class="subsection">`lua_pushcclosure`</span>

<span class="signature">`void lua_pushcclosure(lua_State* L, lua_CFunction fn, const char* debugname, int nup)`</span>
<span class="stack">`[-n, +1, -]`</span>

- `L`: Lua thread
- `fn`: C Function
- `debugname`: Debug name
- `nup`: Number of upvalues to capture


Equivalent to `lua_pushcclosurek`, but without any continuation function provided.


----


### <span class="subsection">`lua_pushcfunction`</span>

<span class="signature">`void lua_pushcfunction(lua_State* L, lua_CFunction fn, const char* debugname)`</span>
<span class="stack">`[-0, +1, -]`</span>

- `L`: Lua thread
- `fn`: C Function
- `debugname`: Debug name


Pushes the C function to the stack.

Equivalent to `lua_pushcclosurek`, but without any upvalues nor any continuation function.

```cpp title="Example" hl_lines="6"
int multiply(lua_State* L) {
	lua_pushnumber(L, lua_tonumber(L, 1) * lua_tonumber(L, 2));
	return 1;
}

lua_pushcfunction(L, multiply, "multiply");
lua_setglobal(L, "multiply");
```

```luau title="Luau Example"
print("2 * 5 = " .. multiply(2, 5))
```


----


### <span class="subsection">`lua_pushthread`</span>

<span class="signature">`int lua_pushthread(lua_State* L)`</span>
<span class="stack">`[-0, +1, -]`</span>

- `L`: Lua thread


Pushes the thread (L) to the stack. Returns `1` if the thread is the main thread, otherwise `0`.

```cpp title="Example" hl_lines="1"
lua_pushthread(L);

lua_State* T = lua_tothread(L, -1);
// T == L
```


----


### <span class="subsection">`lua_createtable`</span>

<span class="signature">`void lua_createtable(lua_State* L, int narr, int nrec)`</span>
<span class="stack">`[-0, +1, -]`</span>

- `L`: Lua thread
- `narr`: Array size
- `nrec`: Dictionary size


Pushes a new table onto the stack, allocating `narr` slots on the array portion and `nrec` slots on the dictionary portion. Use [`lua_newtable`](#lua_newtable) to create a table with zero size allocation, equivalent to `lua_createtable(0, 0)`.

These allocated slots are _not_ filled.

```cpp title="Example"
lua_createtable(L, 10, 0); // Push a new table onto the stack with 10 array slots allocated
// 10 slots allocated, but not filled, e.g. lua_objlen(L, -1) == 0
```


----


### <span class="subsection">`lua_newtable`</span>

<span class="signature">`void lua_newtable(lua_State* L)`</span>
<span class="stack">`[-0, +1, -]`</span>

- `L`: Lua thread


Pushes a new table onto the stack. This is equivalent to `lua_createtable(L, 0, 0)`.


----


## Get Functions

### <span class="subsection">`lua_gettable`</span>

<span class="signature">`int lua_gettable(lua_State* L, int idx)`</span>
<span class="stack">`[-1, +1, -]`</span>

- `L`: Lua thread
- `idx`: Stack index


Pushes a value from a table onto the stack. The table is at index `idx` on the stack, and the key into the table is on the top of the stack. This function pops the key at the top of the stack. The `__index` metamethod may be triggered when using this function.  If this is undesirable, use [`lua_rawget`](#lua_rawget) instead.

Returns the type of the value.

```cpp title="Example"
// Assume the top of the stack is the Luau table: { "hello" = 40 }
lua_pushliteral(L, "hello");
int t = lua_gettable(L, -2); // Our key "hello" is at the top of the stack, and -2 is the table.
// t == LUA_TNUMBER
// lua_tonumber(L, -1) == 40
```


----


### <span class="subsection">`lua_getfield`</span>

<span class="signature">`int lua_getfield(lua_State* L, int idx, const char* k)`</span>
<span class="stack">`[-0, +1, -]`</span>

- `L`: Lua thread
- `idx`: Stack index
- `k`: Field


Pushes a value from a table onto the stack. The table is at index `idx` on the stack, and the key into the table is `k`. The `__index` metamethod may be triggered when using this function. If this is undesirable, use [`lua_rawgetfield`](#lua_rawgetfield) instead.

Returns the type of the value.

```cpp title="Example"
// Assume the top of the stack is the Luau table: { "hello" = 40 }
int t = lua_getfield(L, -2, "hello"); // Our key "hello" is at the top of the stack, and -2 is the table.
// t == LUA_TNUMBER
// lua_tonumber(L, -1) == 40
```


----


### <span class="subsection">`lua_getglobal`</span>

<span class="signature">`int lua_getglobal(lua_State* L, const char* k)`</span>
<span class="stack">`[-0, +1, -]`</span>

- `L`: Lua thread
- `k`: Field


Pushes a value from the global table onto the stack. Use [`lua_setglobal`](#lua_setglobal) to set a new global value.

Returns the type of the value.

```cpp title="Example" hl_lines="4"
lua_pushliteral(L, "hello");
lua_setglobal(L, "message"); // _G.message = "hello"

lua_getglobal(L, "message");
const char* s = lua_tostring(L, -1); // s == "hello"
```


----


### <span class="subsection">`lua_rawgetfield`</span>

<span class="signature">`int lua_rawgetfield(lua_State* L, int idx, const char* k)`</span>
<span class="stack">`[-0, +1, -]`</span>

- `L`: Lua thread
- `idx`: Stack index
- `k`: Field


This is the same as [`lua_getfield`](#lua_getfield), except no `__index` metamethod is ever called.


----


### <span class="subsection">`lua_rawget`</span>

<span class="signature">`int lua_rawget(lua_State* L, int idx)`</span>
<span class="stack">`[-1, +1, -]`</span>

- `L`: Lua thread
- `idx`: Stack index


This is the same as [`lua_gettable`](#lua_gettable), except no `__index` metamethod is ever called.


----


### <span class="subsection">`lua_rawgeti`</span>

<span class="signature">`int lua_rawgeti(lua_State* L, int idx, int n)`</span>
<span class="stack">`[-1, +1, -]`</span>

- `L`: Lua thread
- `idx`: Stack index
- `n`: Table index


Pushes the table value at index `n` onto the stack. The table is located on the stack at `idx`. Similar to `lua_rawget`, no metamethods are called. Note that Luau tables start at index `1`, not `0`.

```cpp title="Example" hl_lines="2"
// Assume the top of the stack is the Luau table: { 5, 15, 30 }
lua_rawgeti(L, -1, 2); // t[2]
double n = lua_tonumber(L, -1);
printf("%f\n", n); // 15
```


----


### <span class="subsection">`lua_setreadonly`</span>

<span class="signature">`void lua_setreadonly(lua_State* L, int idx, int enabled)`</span>
<span class="stack">`[-0, +0, -]`</span>

- `L`: Lua thread
- `idx`: Stack index
- `enabled`: Readonly enabled


Sets the read-only state of a table. Read-only tables ensure that table values cannot be modified, added, or removed. This is only a shallow application, i.e. a nested table may still be writable.

```cpp title="Example" hl_lines="4"
lua_newtable(L);
lua_pushliteral(L, "hello");
lua_rawsetfield(L, -2, "message"); // t.message = "hello"
lua_setreadonly(L, -1, true);
```


----


### <span class="subsection">`lua_getreadonly`</span>

<span class="signature">`int lua_getreadonly(lua_State* L, int idx)`</span>
<span class="stack">`[-0, +0, -]`</span>

- `L`: Lua thread
- `idx`: Stack index


Returns `1` if the table is marked as read-only, otherwise `0`.

```cpp title="Example" hl_lines="4"
// Assume a table is at the top of the stack
if (!lua_getreadonly(L, -1)) {
	// Safe to modify table
}
```


----


### <span class="subsection">`lua_setsafeenv`</span>

<span class="signature">`void lua_setsafeenv(lua_State* L, int idx, int enabled)`</span>
<span class="stack">`[-0, +0, -]`</span>

- `L`: Lua thread
- `idx`: Stack index
- `enabled`: Safe environment enabled


Sets the safe-env state of a thread. TODO.


----


### <span class="subsection">`lua_getsafeenv`</span>

<span class="signature">`int lua_getsafeenv(lua_State* L, int idx)`</span>
<span class="stack">`[-0, +0, -]`</span>

- `L`: Lua thread
- `idx`: Stack index


Gets the safe-env state of a thread. TODO.


----


## Set Functions

### <span class="subsection">`lua_settable`</span>

<span class="signature">`void lua_settable(lua_State* L, int idx)`</span>
<span class="stack">`[-2, +0, -]`</span>

- `L`: Lua thread
- `idx`: Stack index


Sets the value of a table index, e.g. `t[k] = v`, where `t` is located on the stack at `idx`, and the key and value are on the top of the stack.

```cpp title="Example" hl_lines="5"
lua_newtable(L);

lua_pushliteral(L, "hello");
lua_pushinteger(L, 50);
lua_settable(L, -3); // t.hello = 50
```


----


### <span class="subsection">`lua_setfield`</span>

<span class="signature">`void lua_setfield(lua_State* L, int idx, const char* k)`</span>
<span class="stack">`[-1, +0, -]`</span>

- `L`: Lua thread
- `idx`: Stack index
- `k`: Field


Sets the value of a table index, e.g. `t[k] = v`, where `t` is located on the stack at `idx`, and the value is on the top of the stack.

```cpp title="Example" hl_lines="4"
lua_newtable(L);

lua_pushinteger(L, 50);
lua_setfield(L, -2, "hello"); // t.hello = 50
```


----


### <span class="subsection">`lua_setglobal`</span>

<span class="signature">`void lua_setglobal(lua_State* L, const char* k)`</span>
<span class="stack">`[-1, +0, -]`</span>

- `L`: Lua thread
- `k`: Field


Places the value at the top of the stack into the global table at key `k`. The value is popped from the stack. Use [`lua_getglobal`](#lua_getglobal) to retrieve the value.

As implied by the name, globals are globally-accessible to Luau.

```cpp title="Example"
lua_pushliteral(L, "hello");
lua_setglobal(L, "message"); // _G.message = "hello"
```

```luau title="Luau Example"
print(message) -- "hello"
```


----


### <span class="subsection">`lua_rawsetfield`</span>

<span class="signature">`void lua_rawsetfield(lua_State* L, int idx, const char* k)`</span>
<span class="stack">`[-1, +0, -]`</span>

- `L`: Lua thread
- `idx`: Stack index
- `k`: Field


The same as [`lua_setfield`](#lua_setfield), except no metamethods are invoked.


----


### <span class="subsection">`lua_rawset`</span>

<span class="signature">`void lua_rawset(lua_State* L, int idx)`</span>
<span class="stack">`[-2, +0, -]`</span>

- `L`: Lua thread
- `idx`: Stack index


The same as [`lua_settable`](#lua_settable), except no metamethods are invoked.


----


### <span class="subsection">`lua_rawseti`</span>

<span class="signature">`int lua_rawseti(lua_State* L, int idx, int n)`</span>
<span class="stack">`[-1, +0, -]`</span>

- `L`: Lua thread
- `idx`: Stack index
- `n`: Table index


Performs `t[n] = v`, where `t` is the table on the stack at `idx`, and `v` is the value on the top of the stack. The top value is also popped.

```cpp title="Example" hl_lines="5"
lua_newtable(L);

for (int i = 1; i <= 10; i++) {
	lua_pushinteger(L, i * 10);
	lua_rawseti(L, -2, i); // t[i] = i * 10
}
```


----


### <span class="subsection">`lua_setfenv`</span>

<span class="signature">`int lua_setfenv(lua_State* L, int idx)`</span>
<span class="stack">`[-1, +0, -]`</span>

- `L`: Lua thread
- `idx`: Stack index


Sets the environment of the value at `idx` to the table on the top of the stack, and pops this top value. Returns `0` if the value at the given index is not an applicable type for setting an environment (e.g. a number), otherwise returns `1`.


----


## String Functions

### <span class="subsection">`lua_pushliteral`</span>

<span class="signature">`void lua_pushliteral(lua_State* L, const char* str)`</span>
<span class="stack">`[-0, +1, -]`</span>

- `L`: Lua thread
- `str`: C-style string


Pushes the string literal `str` to the stack with a length of `len`.

```cpp title="Example"
lua_pushliteral(L, "hello world");
```


----


### <span class="subsection">`lua_pushlstring`</span>

<span class="signature">`void lua_pushlstring(lua_State* L, const char* str, size_t len)`</span>
<span class="stack">`[-0, +1, -]`</span>

- `L`: Lua thread
- `str`: C-style string
- `len`: String length


Pushes string `str` to the stack with a length of `len`.

Internally, strings in Luau are copied and interned. Thus, modifications made to the inputted string will not be reflected in the Luau string value.

This function is preferred over [`lua_pushstring`](#lua_pushstring) if the string length is known, or if the string contains `\0` characters as part of the string itself.

```cpp title="Example"
std::string str = "hello";
lua_pushlstring(L, str.c_str(), str.size());
```


----


### <span class="subsection">`lua_pushstring`</span>

<span class="signature">`void lua_pushstring(lua_State* L, const char* str)`</span>
<span class="stack">`[-0, +1, -]`</span>

- `L`: Lua thread
- `str`: C-style string


Pushes string `str` to the stack. The length of the string is determined internally using the C `strlen` function.

If the length of the string is known, it is more efficient to use [`lua_pushlstring`](#lua_pushlstring).

Internally, strings in Luau are copied and interned. Thus, modifications made to the inputted string will not be reflected in the Luau string value.

```cpp title="Example"
const char* str = "hello";
lua_pushstring(L, str);
```


----


### <span class="subsection">`lua_pushvfstring`</span>

<span class="signature">`const char* lua_pushvfstring(lua_State* L, const char* fmt, va_list argp)`</span>
<span class="stack">`[-0, +1, -]`</span>

- `L`: Lua thread
- `fmt`: C-style string for formatting
- `argp`: Format arguments


Pushes a string to the stack, where the string is `fmt` formatted against the arguments in `argp`. The formatted string is also returned.

```cpp title="Example"
void format_something(lua_State* L, const char* fmt, ...) {
	va_list args;
	va_start(args, fmt);
	lua_pushvfstring(L, fmt, args);
	va_end(args);
}

format_something(L, "number: %d", 32);
```


----


### <span class="subsection">`lua_pushfstring`</span>

<span class="signature">`const char* lua_pushfstring(lua_State* L, const char* fmt,  ...)`</span>
<span class="stack">`[-0, +1, -]`</span>

- `L`: Lua thread
- `fmt`: C-style string for formatting
- `...`: Format arguments


Pushes a string to the stack, where the string is `fmt` formatted against the arguments. The formatted string is also returned.

```cpp title="Example"
const char* s = lua_pushfstring(L, "number: %d", 32);
```


----


### <span class="subsection">`lua_tolstring`</span>

<span class="signature">`const char* lua_tolstring(lua_State* L, int idx, size_t len)`</span>
<span class="stack">`[-0, +0, m]`</span>

- `L`: Lua thread
- `idx`: Stack index
- `len`: String length


Returns the value at the given stack index converted to a string. The length of the string is written to `len`. Like C strings, Luau strings are terminated with `\0`; however, Luau strings may contain `\0` within the string before the end, thus using the `len` argument is imperative for proper consumption. In other words, functions like `strlen` that scan for `\0` may return lengths that are too short.

**Note:** This will _modify_ the value at the given stack index if it is a number, turning it into a Luau string. If the value at the given stack index is neither a string nor a number, this function will return `NULL`, and the `len` argument will be set to `0`.

```cpp title="Example 1" hl_lines="3 4"
lua_pushliteral(L, "hello world");

size_t len;
const char* msg = lua_tolstring(L, -1, &len);

if (msg) {
	printf("message (len: %zu): \"%s\"\n", len, msg); // message (len: 11) "hello world"
}
```

As noted above, `lua_tolstring` will convert numbers into strings at their given stack index. If this effect is undesirable, either use `lua_isstring()` first, or use the auxilery `luaL_tolstring` function instead.
```cpp title="Example 2"
lua_pushinteger(L, 15);

// The value at index -1 will be converted from a number to a string:
size_t len;
const char* msg = lua_tolstring(L, -1, &len);

printf("Type: %s\n", luaL_typename(L, -1)); // Type: string
```


----


### <span class="subsection">`lua_tostring`</span>

<span class="signature">`const char* lua_tostring(lua_State* L, int idx)`</span>
<span class="stack">`[-0, +0, -]`</span>

- `L`: Lua thread
- `idx`: Stack index


Equivalent to [`lua_tolstring`](#lua_tolstring), without the length argument.


----


### <span class="subsection">`lua_tostringatom`</span>

<span class="signature">`const char* lua_tostringatom(lua_State* L, int idx, int* atom)`</span>
<span class="stack">`[-0, +0, m]`</span>

- `L`: Lua thread
- `idx`: Stack index
- `atom`: Atom


Identical to [`lua_tostring`](#lua_tostring), except the string atom is written to the `atom` argument. See the [Atoms](guide/atoms.md) page for more information on string atoms.


----


### <span class="subsection">`lua_tolstringatom`</span>

<span class="signature">`const char* lua_tolstringatom(lua_State* L, int idx, size_t len, int* atom)`</span>
<span class="stack">`[-0, +0, m]`</span>

- `L`: Lua thread
- `idx`: Stack index
- `len`: String length
- `atom`: Atom


Identical to [`lua_tolstring`](#lua_tolstring), except the string atom is written to the `atom` argument. See the [Atoms](guide/atoms.md) page for more information on string atoms.


----


### <span class="subsection">`lua_strlen`</span>

<span class="signature">`int lua_strlen(lua_State* L, int idx)`</span>
<span class="stack">`[-0, +0, -]`</span>

- `L`: Lua thread
- `idx`: Stack index


Alias for [`lua_objlen`](#lua_objlen).


----


### <span class="subsection">`lua_isstring`</span>

<span class="signature">`int lua_isstring(lua_State* L, int idx)`</span>
<span class="stack">`[-0, +0, -]`</span>

- `L`: Lua thread
- `idx`: Stack index


Returns `1` if the value at the given stack index is a string _or_ a number (all numbers can be converted to a string). Otherwise, returns `0`.


----


### <span class="subsection">`luaL_tolstring`</span>

<span class="signature">`const char* luaL_tolstring(lua_State* L, int idx, size_t len)`</span>
<span class="stack">`[-0, +1, -]`</span>

- `L`: Lua thread
- `idx`: Stack index
- `len`: String length


Converts the value at the given index into a string. This string is both pushed onto the stack and returned. Unlike `lua_tolstring` and `lua_tostring`, this function does _not_ modify the value at the given stack index.

```cpp title="Example" hl_lines="2"
lua_pushvector(L, 10, 20, 30);
const char* vstr = lua_tolstring(L, -1, nullptr);
lua_pop(L, 1); // pop vstr from the stack
printf("vector: %s\n", vstr); // "vector: 10, 20, 30"
```


----


### <span class="subsection">`luaL_checklstring`</span>

<span class="signature">`const char* luaL_checklstring(lua_State* L, int idx, size_t len)`</span>
<span class="stack">`[-0, +0, -]`</span>

- `L`: Lua thread
- `idx`: Stack index
- `len`: String length


Similar to [`lua_tolstring`](#lua_tolstring), except the type will be asserted. If the value is not a string, an error will be thrown.

```cpp title="Example"
int send_message(lua_State* L) {
	size_t message_len;
	const char* message = luaL_checklstring(L, 1, &message_len);
}
```


----


### <span class="subsection">`luaL_checkstring`</span>

<span class="signature">`const char* luaL_checkstring(lua_State* L, int idx)`</span>
<span class="stack">`[-0, +0, -]`</span>

- `L`: Lua thread
- `idx`: Stack index


Equivalent to [`luaL_checklstring(L, idx, nullptr)`](#lual_checklstring).


----


### <span class="subsection">`luaL_optlstring`</span>

<span class="signature">`const char* luaL_optlstring(lua_State* L, int idx, const char* def, size_t len)`</span>
<span class="stack">`[-0, +0, -]`</span>

- `L`: Lua thread
- `idx`: Stack index
- `def`: Default string
- `len`: String length


Gets the string at the given stack index. If the value at the given index is nil or none, then `def` is returned instead. Otherwise, an error is thrown.

```cpp title="Example"
int send_message(lua_State* L) {
	size_t message_len;
	const char* message = luaL_optlstring(L, 1, "Default message", &message_len);
}
```


----


### <span class="subsection">`luaL_optstring`</span>

<span class="signature">`const char* luaL_optstring(lua_State* L, int idx, const char* def)`</span>
<span class="stack">`[-0, +0, -]`</span>

- `L`: Lua thread
- `idx`: Stack index
- `def`: Default string


Equivalent to [`luaL_optlstring(L, idx, def, nullptr)`](#lual_optlstring).


----


## Number Functions

### <span class="subsection">`lua_pushnumber`</span>

<span class="signature">`void lua_pushnumber(lua_State* L, double n)`</span>
<span class="stack">`[-0, +1, -]`</span>

- `L`: Lua thread
- `n`: Number


Pushes `n` to the stack.

```cpp title="Example"
lua_pushnumber(L, 15.2);
```


----


### <span class="subsection">`lua_pushinteger`</span>

<span class="signature">`void lua_pushinteger(lua_State* L, int n)`</span>
<span class="stack">`[-0, +1, -]`</span>

- `L`: Lua thread
- `n`: Number


Pushes `n` to the stack. Note that all Luau numbers are doubles, so the value of `n` will be cast to a `double`.

```cpp title="Example"
lua_pushinteger(L, 32);
```


----


### <span class="subsection">`lua_pushunsigned`</span>

<span class="signature">`void lua_pushunsigned(lua_State* L, unsigned int n)`</span>
<span class="stack">`[-0, +1, -]`</span>

- `L`: Lua thread
- `n`: Number


Pushes `n` to the stack. Note that all Luau numbers are doubles, so the value of `n` will be cast to a `double`.

```cpp title="Example"
lua_pushunsigned(L, 32);
```


----


### <span class="subsection">`lua_tonumberx`</span>

<span class="signature">`double lua_tonumberx(lua_State* L, int idx, int* isnum)`</span>
<span class="stack">`[-0, +0, -]`</span>

- `L`: Lua thread
- `idx`: Stack index
- `isnum`: Is number


Returns the number at the given stack index. If the value on the stack is a string, Luau will attempt to convert the string to a number.

If the value is a number, or successfully converted to a number, the `isnum` argument will be set to `1`, otherwise `0`.

```cpp title="Example" hl_lines="9 15 21"
lua_pushliteral(L, "hello");
lua_pushliteral(L, "12.5");
lua_pushnumber(L, 15);

double n;
int isnum;

// isnum will be false, since "hello" cannot be converted to a number:
n = lua_tonumberx(L, -3, &isnum);
if (isnum) {
	printf("n: %f\n", n);
}

// isnum is true, and "12.5" is converted to 12.5:
n = lua_tonumberx(L, -2, &isnum);
if (isnum) {
	printf("n: %f\n", n);
}

// isnum is true, and the value is 15:
n = lua_tonumberx(L, -1, &isnum);
if (isnum) {
	printf("n: %f\n", n);
}
```


----


### <span class="subsection">`lua_tonumber`</span>

<span class="signature">`double lua_tonumber(lua_State* L, int idx)`</span>
<span class="stack">`[-0, +0, -]`</span>

- `L`: Lua thread
- `idx`: Stack index


Returns the number at the given stack index. If the value on the stack is a string, Luau will attempt to convert the string to a number. Identical to [`lua_tonumberx`](#lua_tonumberx), without the last `isnum` argument.


----


### <span class="subsection">`lua_tointegerx`</span>

<span class="signature">`int lua_tointegerx(lua_State* L, int idx, int* isnum)`</span>
<span class="stack">`[-0, +0, -]`</span>

- `L`: Lua thread
- `idx`: Stack index
- `isnum`: Is number


Returns the number at the given stack index as an integer. If the value on the stack is a string, Luau will attempt to convert the string to an integer. Numbers in Luau are all doubles, so the returned value is cast to an int.

If the value is a number, or successfully converted to a number, the `isnum` argument will be set to `1`, otherwise `0`.

```cpp title="Example" hl_lines="9 15 21"
lua_pushliteral(L, "hello");
lua_pushliteral(L, "12.5");
lua_pushinteger(L, 15);

int n;
int isnum;

// isnum will be false, since "hello" cannot be converted to a number:
n = lua_tointegerx(L, -3, &isnum);
if (isnum) {
	printf("n: %d\n", n);
}

// isnum is true, and "12.5" is converted to 12:
n = lua_tointegerx(L, -2, &isnum);
if (isnum) {
	printf("n: %d\n", n);
}

// isnum is true, and the value is 15:
n = lua_tointegerx(L, -1, &isnum);
if (isnum) {
	printf("n: %d\n", n);
}
```


----


### <span class="subsection">`lua_tointeger`</span>

<span class="signature">`int lua_tointeger(lua_State* L, int idx)`</span>
<span class="stack">`[-0, +0, -]`</span>

- `L`: Lua thread
- `idx`: Stack index


Returns the number at the given stack index as an integer. If the value on the stack is a string, Luau will attempt to convert the string to an integer. Numbers in Luau are all doubles, so the returned value is cast to an int. Identical to [`lua_tointegerx`](#lua_tointegerx), without the last `isnum` argument.


----


### <span class="subsection">`lua_tounsignedx`</span>

<span class="signature">`unsigned lua_tounsignedx(lua_State* L, int idx, int* isnum)`</span>
<span class="stack">`[-0, +0, -]`</span>

- `L`: Lua thread
- `idx`: Stack index
- `isnum`: Is number


Returns the number at the given stack index as an unsigned integer. If the value on the stack is a string, Luau will attempt to convert the string to an integer. Numbers in Luau are all doubles, so the returned value is cast to an unsigned int.

If the value is a number, or successfully converted to a number, the `isnum` argument will be set to `1`, otherwise `0`.

```cpp title="Example" hl_lines="9 15 21"
lua_pushliteral(L, "hello");
lua_pushliteral(L, "12.5");
lua_pushunsigned(L, 15);

unsigned n;
int isnum;

// isnum will be false, since "hello" cannot be converted to a number:
n = lua_tounsignedx(L, -3, &isnum);
if (isnum) {
	printf("n: %d\n", n);
}

// isnum is true, and "12.5" is converted to 12:
n = lua_tounsignedx(L, -2, &isnum);
if (isnum) {
	printf("n: %d\n", n);
}

// isnum is true, and the value is 15:
n = lua_tounsignedx(L, -1, &isnum);
if (isnum) {
	printf("n: %d\n", n);
}
```


----


### <span class="subsection">`lua_tounsigned`</span>

<span class="signature">`unsigned lua_tounsigned(lua_State* L, int idx)`</span>
<span class="stack">`[-0, +0, -]`</span>

- `L`: Lua thread
- `idx`: Stack index


Returns the number at the given stack index as an unsigned integer. If the value on the stack is a string, Luau will attempt to convert the string to an integer. Numbers in Luau are all doubles, so the returned value is cast to an unsigned int. Identical to [`lua_tounsignedx`](#lua_tounsignedx), without the last `isnum` argument.


----


### <span class="subsection">`lua_isnumber`</span>

<span class="signature">`int lua_isnumber(lua_State* L, int idx)`</span>
<span class="stack">`[-0, +0, -]`</span>

- `L`: Lua thread
- `idx`: Stack index


Returns `1` if the value at stack index `idx` is a number _or_ the value is a string that can be coerced to a number. Otherwise, returns `0`.


----


### <span class="subsection">`luaL_checknumber`</span>

<span class="signature">`double luaL_checknumber(lua_State* L, int idx)`</span>
<span class="stack">`[-0, +0, -]`</span>

- `L`: Lua thread
- `idx`: Stack index


Returns the number at the given stack index. If the value is not a number, an error is thrown.

```cpp title="Example"
int add(lua_State* L) {
	double lhs = luaL_checknumber(L, 1);
	double rhs = luaL_checknumber(L, 2);

	lua_pushnumber(L, lhs + rhs);
	return 1;
}
```


----


### <span class="subsection">`luaL_checkinteger`</span>

<span class="signature">`int luaL_checkinteger(lua_State* L, int idx)`</span>
<span class="stack">`[-0, +0, -]`</span>

- `L`: Lua thread
- `idx`: Stack index


Returns the number (cast to `int`) at the given stack index. If the value is not a number, an error is thrown.

```cpp title="Example"
int add_int(lua_State* L) {
	int lhs = luaL_checkinteger(L, 1);
	int rhs = luaL_checkinteger(L, 2);

	lua_pushinteger(L, lhs + rhs);
	return 1;
}
```


----


### <span class="subsection">`luaL_checkunsigned`</span>

<span class="signature">`unsigned luaL_checkunsigned(lua_State* L, int idx)`</span>
<span class="stack">`[-0, +0, -]`</span>

- `L`: Lua thread
- `idx`: Stack index


Returns the number (cast to `unsigned`) at the given stack index. If the value is not a number, an error is thrown.

```cpp title="Example"
int add_int(lua_State* L) {
	unsigned lhs = luaL_checkunsigned(L, 1);
	unsigned rhs = luaL_checkunsigned(L, 2);

	lua_pushunsigned(L, lhs + rhs);
	return 1;
}
```


----


### <span class="subsection">`luaL_optnumber`</span>

<span class="signature">`double luaL_optnumber(lua_State* L, int idx, double def)`</span>
<span class="stack">`[-0, +0, -]`</span>

- `L`: Lua thread
- `idx`: Stack index
- `def`: Default


Returns the number at the given stack index, or the default number if the value at the stack index is nil or none. Otherwise, an error is thrown.

```cpp title="Example" hl_lines="5"
int approx_equal(lua_State* L) {
	double a = luaL_checknumber(L, 1);
	double b = luaL_checknumber(L, 2);

	double epsilon = luaL_optnumber(L, 3, 0.00001);

	lua_pushboolean(L, fabs(a - b) < epsilon);
	return 1;
}
```


----


### <span class="subsection">`luaL_optinteger`</span>

<span class="signature">`int luaL_optinteger(lua_State* L, int idx, int def)`</span>
<span class="stack">`[-0, +0, -]`</span>

- `L`: Lua thread
- `idx`: Stack index
- `def`: Default


Returns the number (cast to `int`) at the given stack index, or the default number if the value at the stack index is nil or none. Otherwise, an error is thrown.


----


### <span class="subsection">`luaL_optunsigned`</span>

<span class="signature">`unsigned luaL_optunsigned(lua_State* L, int idx, unsigned def)`</span>
<span class="stack">`[-0, +0, -]`</span>

- `L`: Lua thread
- `idx`: Stack index
- `def`: Default


Returns the number (cast to `unsigned`) at the given stack index, or the default number if the value at the stack index is nil or none. Otherwise, an error is thrown.


----


## Boolean Functions

### <span class="subsection">`lua_pushboolean`</span>

<span class="signature">`void lua_pushboolean(lua_State* L, int b)`</span>
<span class="stack">`[-0, +1, -]`</span>

- `L`: Lua thread
- `b`: Boolean


Pushes boolean `b` to the stack.

```cpp title="Example"
lua_pushboolean(L, true);
lua_pushboolean(L, false);
```


----


### <span class="subsection">`lua_toboolean`</span>

<span class="signature">`int lua_toboolean(lua_State* L, int idx)`</span>
<span class="stack">`[-0, +0, -]`</span>

- `L`: Lua thread
- `idx`: Stack index


Returns `1` if the Luau value at the given stack index is truthy, otherwise returns `0`.

A "falsey" value in Luau is any value that is either `nil` or `false`. All other values are evaluated as `true`. In other languages, values like `0` or empty strings might be evaluated as `false`. This is _not_ the case in Luau. _Only_ `nil` and `false` are evaluated as `false`; all other values are evaluated as `true`.

```cpp title="Example"
lua_pushboolean(L, true);
lua_pushboolean(L, false);
lua_pushnil(L);
lua_pushinteger(L, 0);

if (lua_toboolean(L, -4)) {} // true
if (lua_toboolean(L, -3)) {} // false
if (lua_toboolean(L, -2)) {} // false (nil is evaluated as false)
if (lua_toboolean(L, -1)) {} // true (0 is neither nil or false, so it is evaluated as true in Luau)
```


----


### <span class="subsection">`lua_isboolean`</span>

<span class="signature">`int lua_isboolean(lua_State* L, int idx)`</span>
<span class="stack">`[-0, +0, -]`</span>

- `L`: Lua thread
- `idx`: Stack index


Checks if the value at the given stack index is a boolean.

```cpp title="Example"
if (lua_isboolean(L, -1)) { /* ... */ }
```


----


### <span class="subsection">`luaL_checkboolean`</span>

<span class="signature">`int luaL_checkboolean(lua_State* L, int idx)`</span>
<span class="stack">`[-0, +0, -]`</span>

- `L`: Lua thread
- `idx`: Stack index


Returns `1` if the Luau value at the given stack index is true, otherwise returns `0`. Throws an error if the value at the given index is not a boolean.

**Note:** Unlike `lua_toboolean`, this is not a _truthy/falsey_ check. The value at the given index must be a boolean.


----


### <span class="subsection">`luaL_optboolean`</span>

<span class="signature">`int luaL_optboolean(lua_State* L, int idx, int def)`</span>
<span class="stack">`[-0, +0, -]`</span>

- `L`: Lua thread
- `idx`: Stack index
- `def`: Default


Returns `1` or `0` for the given boolean value. Returns `def` if the value at the given index is nil or none. Otherwise, an error is thrown.

**Note:** Unlike `lua_toboolean`, this is not a _truthy/falsey_ check. The value at the given index must be a boolean.


----


## Vector Functions

### <span class="subsection">`lua_pushvector`</span>

<span class="signature">`void lua_pushvector(lua_State* L, float x, float y, float z)`</span>
<span class="stack">`[-0, +1, -]`</span>

- `L`: Lua thread
- `x`: X
- `y`: Y
- `z`: Z


Pushes a vector to the Luau stack. Luau comes with a [vector library](https://luau.org/library#vector-library) for operating against vector values.

**Note:** Unlike Luau numbers being double-precision floating point numbers, Luau vector values are single-precision floats.

```cpp title="Example 3-wide" hl_lines="1"
// By default, Luau vectors are 3-wide

lua_pushvector(L, 10, 15, 20);

const char* v = lua_tovector(L, -1);
float x = v[0]; // 10
float y = v[1]; // 15
float z = v[2]; // 20
```

If Luau is built with the `LUA_VECTOR_SIZE` preprocessor set to `4`, then this will be a 4-wide vector, and the function will have an additional `w` parameter.
```cpp title="Example 4-wide" hl_lines="1"
// If Luau is built with LUA_VECTOR_SIZE=4

lua_pushvector(L, 10, 15, 20, 25);

const char* v = lua_tovector(L, -1);
float x = v[0]; // 10
float y = v[1]; // 15
float z = v[2]; // 20
float w = v[3]; // 25
```


----


### <span class="subsection">`lua_tovector`</span>

<span class="signature">`const float* lua_tovector(lua_State* L, int idx)`</span>
<span class="stack">`[-0, +0, -]`</span>

- `L`: Lua thread
- `idx`: Stack index


Returns the vector at the given Luau index, or `NULL` if not a vector.

By default, vectors in Luau are 3-wide. Luau can be built with the `LUA_VECTOR_SIZE` preprocessor set to `4` for 4-wide vectors.

```cpp title="Example" hl_lines="3"
lua_pushvector(L, 3, 5, 2); // x, y, z

const float* vec = lua_tovector(L, -1);

float x = vec[0];
float y = vec[1];
float z = vec[2];
printf("%f, %f, %f\n", x, y, z);
```


----


### <span class="subsection">`lua_isvector`</span>

<span class="signature">`int lua_isvector(lua_State* L, int idx)`</span>
<span class="stack">`[-0, +0, -]`</span>

- `L`: Lua thread
- `idx`: Stack index


Checks if the value at the given stack index is a vector.

```cpp title="Example"
if (lua_isvector(L, -1)) { /* ... */ }
```


----


### <span class="subsection">`luaL_checkvector`</span>

<span class="signature">`const float* luaL_checkvector(lua_State* L, int idx)`</span>
<span class="stack">`[-0, +0, -]`</span>

- `L`: Lua thread
- `idx`: Stack index


Returns the vector at the given Luau index. If the value at the given index is not a vector, an error is thrown.


----


### <span class="subsection">`luaL_optvector`</span>

<span class="signature">`const float* luaL_optvector(lua_State* L, int idx, const float* def)`</span>
<span class="stack">`[-0, +0, -]`</span>

- `L`: Lua thread
- `idx`: Stack index
- `def`: Default


Returns the vector at the given Luau index. If the value at the given index is nil or none, then `def` is returned. Otherwise, an error is thrown.


----


## Buffer Functions

### <span class="subsection">`lua_newbuffer`</span>

<span class="signature">`void* lua_newbuffer(lua_State* L, size_t sz)`</span>
<span class="stack">`[-0, +1, -]`</span>

- `L`: Lua thread
- `sz`: Size


Pushes a new buffer to the stack and returns a pointer to the buffer. Buffers are just arbitrary data. Luau can create and interact with buffers through the [`buffer` library](https://luau.org/library#buffer-library). Use the [`lua_tobuffer`](#lua_tobuffer) function to retrieve a buffer from the stack.

```cpp title="Example" hl_lines="8"
struct Foo {
	int n;
}

// As an example, write 'Foo' to a buffer:
Foo foo{};
foo.n = 10;
void* buf = lua_newbuffer(L, sizeof(Foo));
memcpy(buf, &foo, sizeof(Foo));
```


----


### <span class="subsection">`lua_tobuffer`</span>

<span class="signature">`void* lua_tobuffer(lua_State* L, int idx)`</span>
<span class="stack">`[-0, +0, -]`</span>

- `L`: Lua thread
- `idx`: Stack index


Returns the buffer at the given stack index, or `NULL` if the value is not a buffer.

```cpp title="Example" hl_lines="4"
void* buf = lua_newbuffer(L, 10);

size_t len;
void* b = lua_tobuffer(L, -1, &len);
// b == buf
// len == 10
```


----


### <span class="subsection">`lua_isbuffer`</span>

<span class="signature">`int lua_isbuffer(lua_State* L, int idx)`</span>
<span class="stack">`[-0, +0, -]`</span>

- `L`: Lua thread
- `idx`: Stack index


Checks if the value at the given stack index is a buffer.

```cpp title="Example"
if (lua_isbuffer(L, -1)) { /* ... */ }
```


----


### <span class="subsection">`luaL_checkbuffer`</span>

<span class="signature">`void* luaL_checkbuffer(lua_State* L, int idx)`</span>
<span class="stack">`[-0, +0, -]`</span>

- `L`: Lua thread
- `idx`: Stack index


Returns the buffer at the given stack index. If the value retrieved is not a buffer, an error is thrown.


----


## Metatable Functions

### <span class="subsection">`lua_setmetatable`</span>

<span class="signature">`int lua_setmetatable(lua_State* L, int idx)`</span>
<span class="stack">`[-1, +0, -]`</span>

- `L`: Lua thread
- `idx`: Stack index


Takes the table at the top of the stack and assigns it as the metatable of the table on the stack at `idx`.

The return value can be ignored; this function always returns `1`.

```cpp title="Example" hl_lines="7"
// Create table:
lua_newtable(L); // t

// Create metatable:
lua_newtable(L); // mt
lua_pushliteral("v");
lua_rawsetfield(L, -2, "__mode"); // mt.__mode = "v"
lua_setmetatable(L, -2); // setmetatable(t, mt)
```


----


### <span class="subsection">`lua_getmetatable`</span>

<span class="signature">`int lua_getmetatable(lua_State* L, int idx)`</span>
<span class="stack">`[-0, +(0|1), -]`</span>

- `L`: Lua thread
- `idx`: Stack index


Gets the metatable for the object at the given stack index. If the metatable is found, it is pushed to the top of the stack and the function returns `1`. Otherwise, the function returns `0` and the stack remains the same.

```cpp title="Example"
if (lua_getmetatable(L, -1)) {
	// Metatable is now at the top of the stack
}
```


----


### <span class="subsection">`lua_setuserdatametatable`</span>

<span class="signature">`void lua_setuserdatametatable(lua_State* L, int tag)`</span>
<span class="stack">`[-1, +0, -]`</span>

- `L`: Lua thread
- `tag`: Tag


Pops the value (expecting a table) at the top of the stack and sets the userdata metatable for the given userdata tag. This is used in conjunction with [`lua_newuserdatataggedwithmetatable`](#lua_newuserdatataggedwithmetatable). See the example there.

This function can only be called once per tag. Calling this function again for the same tag will throw an error.


----


### <span class="subsection">`lua_getuserdatametatable`</span>

<span class="signature">`void lua_getuserdatametatable(lua_State* L, int tag)`</span>
<span class="stack">`[-0, +1, -]`</span>

- `L`: Lua thread
- `tag`: Tag


Pushes the metatable associated with the userdata tag onto the stack (or `nil` if there is no associated metatable).


----


### <span class="subsection">`lua_getmetafield`</span>

<span class="signature">`int lua_getmetafield(lua_State* L, int idx, const char* field)`</span>
<span class="stack">`[-0, +(0|1), -]`</span>

- `L`: Lua thread
- `idx`: Stack index
- `field`: Metatable field


Attempts to get the given metatable field for the table at `idx`. If the table doesn't have a metatable, or the metatable doesn't have `field`, then this function returns `0` and nothing is pushed onto the stack. Otherwise, the function returns `1` and the field is pushed onto the stack.

```cpp title="Example"
// Assume the top of the stack is a table

if (lua_getmetafield(L, -1, "__index")) {
	// ...
}
```


----


### <span class="subsection">`lua_callmeta`</span>

<span class="signature">`int lua_callmeta(lua_State* L, int idx, const char* field)`</span>
<span class="stack">`[-0, +(0|1), -]`</span>

- `L`: Lua thread
- `idx`: Stack index
- `field`: Metatable field


Attempts to call the given metatable function for the table at `idx`. If the table doesn't have a metatable, or the metatable doesn't have `field`, then this function returns `0` and nothing is pushed onto the stack. Otherwise, the function returns `1` and the result of the called metatable function is pushed onto the stack.

```cpp title="Example"
// Assume the top of the stack is a table

if (lua_callmeta(L, -1, "__tostring")) {
	const char* result = lua_tostring(L, -1);
	lua_pop(L, 1);
	// ...
}
```


----


### <span class="subsection">`luaL_newmetatable`</span>

<span class="signature">`int luaL_newmetatable(lua_State* L, const char* name)`</span>
<span class="stack">`[-1, +0, -]`</span>

- `L`: Lua thread
- `name`: Name


Creates (or fetches existing) metatable with a given name and pushes the metatable onto the stack. Returns `1` if the metatable was created, or `0` if the metatable aleady exists. This is useful for creating metatables linked to specific userdata types.

```cpp title="Example" hl_lines="5"
struct Foo {};

Foo* foo = static_cast<Foo*>(lua_newuserdata(L, sizeof(Foo)));

if (luaL_newmetatable(L, "Foo")) {
	// Build metatable:
	lua_pushliteral(L, "Foo");
	lua_rawsetfield(L, -2, "__type");
}
lua_setmetatable(L, -2);
```


----


### <span class="subsection">`luaL_getmetatable`</span>

<span class="signature">`int luaL_getmetatable(lua_State* L, const char* name)`</span>
<span class="stack">`[-0, +1, -]`</span>

- `L`: Lua thread
- `name`: Name


Attempts to get a metatable from the registry with the given name and pushes it to the stack. If no metatable is found, `nil` will be pushed to the stack. See [`luaL_newmetatable`](#lual_newmetatable).

```cpp title="Example" hl_lines="16-17"
struct Foo {};

Foo* new_Foo() {
	Foo* foo = static_cast<Foo*>(lua_newuserdata(L, sizeof(Foo)));
	if (luaL_newmetatable(L, "Foo")) {
		// Build metatable:
		lua_pushliteral(L, "Foo");
		lua_rawsetfield(L, -2, "__type");
	}
	lua_setmetatable(L, -2);
	return foo;
}

// ...

// Get the metatable created with `luaL_newmetatable`:
luaL_getmetatable(L, "Foo");
```


----


## Userdata Functions

### <span class="subsection">`lua_newuserdata`</span>

<span class="signature">`void* lua_newuserdata(lua_State* L, size_t sz)`</span>
<span class="stack">`[-0, +1, -]`</span>

- `L`: Lua thread
- `sz`: Size of the data


Creates a userdata and pushes it to the stack. A pointer to the newly-constructed data is returned. This is equivalent to `lua_newuserdatatagged` with a tag of `0`.

**Note:** Luau-constructed userdata are not zero-initialized. After construction, assign all fields of the object.

```cpp title="Example" hl_lines="5"
struct Foo {
	int n;
};

Foo* foo = static_cast<Foo*>(lua_newuserdata(L, sizeof(Foo)));

// Before explicit assignment, `n` is garbage, so we should initialize it ourselves:
foo->n = 0;
```


----


### <span class="subsection">`lua_newuserdatadtor`</span>

<span class="signature">`void* lua_newuserdatadtor(lua_State* L, size_t sz, void (*dtor)(void*))`</span>
<span class="stack">`[-0, +1, -]`</span>

- `L`: Lua thread
- `sz`: Size of the data
- `dtor`: Destructor


Creates a new userdata with an assigned destructor. Destructors are called when Luau is freeing up the userdata memory.

To assign a destructor for all userdata of a given tag, use [`lua_setuserdatadtor`](#lua_setuserdatadtor).

```cpp title="Example" hl_lines="5-9"
struct Foo {
	char* data;
};

Foo* foo = static_cast<Foo*>(lua_newuserdatadtor(L, sizeof(Foo), [](void* ptr) {
	// This function is called when Foo is being GC'd. Free up any user-managed resources now.
	Foo* f = static_cast<Foo*>(ptr);
	delete[] f->data;
}));

foo->data = new char[256];
```


----


### <span class="subsection">`lua_newuserdatatagged`</span>

<span class="signature">`void* lua_newuserdatatagged(lua_State* L, size_t sz, int tag)`</span>
<span class="stack">`[-0, +1, -]`</span>

- `L`: Lua thread
- `sz`: Size of the data
- `tag`: Tag


Creates the tagged userdata and pushes it to the stack. A pointer to the newly-constructed data is returned. Use [`lua_touserdatatagged`](#lua_touserdatatagged) to retrieve the value. For more info on tags, see the [Tags](guide/tags.md) page.

**Note:** Luau-constructed userdata are not zero-initialized. After construction, assign all fields of the object.

```cpp title="Example" hl_lines="6"
constexpr int kFooTag = 1;
struct Foo {
	int n;
};

Foo* foo = static_cast<Foo*>(lua_newuserdatatagged(L, sizeof(Foo), kFooTag));

// Before explicit assignment, `n` is garbage, so we should initialize it ourselves:
foo->n = 0;
```


----


### <span class="subsection">`lua_newuserdatataggedwithmetatable`</span>

<span class="signature">`void* lua_newuserdatataggedwithmetatable(lua_State* L, size_t sz, int tag)`</span>
<span class="stack">`[-0, +1, -]`</span>

- `L`: Lua thread
- `sz`: Size of the data
- `tag`: Tag


Creates the tagged userdata with a pre-defined metatable and pushes it to the stack. A pointer to the newly-constructed data is returned. Use [`lua_touserdatatagged`](#lua_touserdatatagged) to retrieve the value. For more info on tags, see the [Tags](guide/tags.md) page.

Using this method is faster than attempting to assign a metatable to new userdata every construction, e.g. using `luaL_newmetatable`. Instead, the metatable is created ahead of time using `lua_setuserdatametatable`, linked to the userdata's tag.

```cpp title="Example" hl_lines="35"
constexpr int kFooTag = 1;

struct Foo {
	int n;
};

int Foo_index(lua_State* L) {
	Foo* foo = static_cast<Foo*>(luaL_touserdatatagged(L, 1, kFooTag));
	const char* property = lua_tostring(L, 2);
	if (property && strcmp(property, "n") == 0) {
		lua_pushinteger(L, foo->n);
		return 1;
	}
	luaL_error(L, "unknown property");
}

int Foo_newindex(lua_State* L) {
	Foo* foo = static_cast<Foo*>(luaL_touserdatatagged(L, 1, kFooTag));
	const char* property = lua_tostring(L, 2);
	if (property && strcmp(property, "n") == 0) {
		int new_n = luaL_checkinteger(L, 3);
		foo->n = new_n;
		return 0;
	}
	luaL_error(L, "unknown property");
}

const luaL_Reg Foo_metatable[] = {
	{"__index", Foo_index},
	{"__newindex", Foo_newindex},
	{nullptr, nullptr},
};

int push_Foo() {
	Foo* foo = static_cast<Foo*>(lua_newuserdatataggedwithmetatable(L, sizeof(Foo), kFooTag));
	foo->n = 0;
	return 1;
}

// Called during some initialization period
void setup() {
	luaL_newmetatable(L, "Foo");
	luaL_register(L, nullptr, Foo_metatable);
	lua_setuserdatametatable(L, kFooTag);

	lua_setglobal("new_foo", push_Foo);
}
```

```lua
local foo = new_foo()
foo.n = 55
print(foo.n) -- 55
```


----


### <span class="subsection">`lua_touserdata`</span>

<span class="signature">`void* lua_touserdata(lua_State* L, int idx)`</span>
<span class="stack">`[-0, +0, -]`</span>

- `L`: Lua thread
- `idx`: Stack index


Returns a pointer to a userdata on the stack. Returns `NULL` if the value is not a userdata.

If it is preferred to throw an error if the value is not a userdata, use the `luaL_checkuserdata` function instead.

**Note:** It may be unsafe to hang onto a pointer to a userdata value. The Luau GC owns the userdata memory, and may free it. See the page on [pinning](guide/pinning.md) for tips on keeping a value from being GC'd, or consider using [light userdata](guide/light-userdata.md) instead.

```cpp title="Example" hl_lines="8"
struct Foo {
	int n;
};

Foo* foo = static_cast<Foo*>(lua_newuserdata(L, sizeof(Foo)));
foo->n = 32;

Foo* f = static_cast<Foo*>(lua_touserdata(L, -1));
printf("foo->n = %d\n", foo->n); // foo->n = 32
```


----


### <span class="subsection">`lua_touserdatatagged`</span>

<span class="signature">`void* lua_touserdatatagged(lua_State* L, int idx, int tag)`</span>
<span class="stack">`[-0, +0, -]`</span>

- `L`: Lua thread
- `idx`: Stack index
- `tag`: Tag


Returns a pointer to a tagged userdata on the stack. Returns `NULL` if the value is not a userdata _or_ the userdata's tag does not match the provided `tag` argument. For more info on tags, see the [Tags](guide/tags.md) page.

**Note:** It may be unsafe to hang onto a pointer to a userdata value. The Luau GC owns the userdata memory, and may free it. See the page on [pinning](guide/pinning.md) for tips on keeping a value from being GC'd, or consider using [light userdata](guide/light-userdata.md) instead.

```cpp title="Example" hl_lines="10"
constexpr int kFooTag = 1;

struct Foo {
	int n;
};

Foo* foo = static_cast<Foo*>(lua_newuserdatatagged(L, sizeof(Foo), kFooTag));
foo->n = 32;

Foo* f = static_cast<Foo*>(lua_touserdatatagged(L, -1, kFooTag));
printf("foo->n = %d\n", foo->n); // foo->n = 32
```


----


### <span class="subsection">`lua_setuserdatatag`</span>

<span class="signature">`int lua_setuserdatatag(lua_State* L, int idx, int tag)`</span>
<span class="stack">`[-0, +0, -]`</span>

- `L`: Lua thread
- `idx`: Stack index
- `tag`: Tag


Sets the tag for userdata at stack index `idx`. Alternatively, the [`lua_newuserdatatagged`](#lua_newuserdatatagged) and [`lua_newuserdatataggedwithmetatable`](#lua_newuserdatataggedwithmetatable) functions can be used to assign the tag on userdata creation.


----


### <span class="subsection">`lua_userdatatag`</span>

<span class="signature">`int lua_userdatatag(lua_State* L, int idx)`</span>
<span class="stack">`[-0, +0, -]`</span>

- `L`: Lua thread
- `idx`: Stack index


Returns the tag for the userdata at the given stack position. For non-userdata values, this function returns `-1`. If the userdata value was not assigned a tag, the tag will be set to the default of `0`, and thus this function will return `0`.

```cpp title="Example" hl_lines="12-14"
constexpr int kFooTag = 10;
constexpr int kBarTag = 20;

struct Foo {};
struct Bar {};
struct Baz {};

lua_pushuserdatatagged(L, sizeof(Foo), kFooTag);
lua_pushuserdatatagged(L, sizeof(Bar), kBarTag);
lua_pushuserdata(L, sizeof(Baz));

int foo_tag = lua_userdatatag(L, -3); // 10
int bar_tag = lua_userdatatag(L, -2); // 20
int baz_tag = lua_userdatatag(L, -1); // 0
```


----


### <span class="subsection">`lua_setuserdatadtor`</span>

<span class="signature">`int lua_setuserdatadtor(lua_State* L, int tag, lua_Destructor dtor)`</span>
<span class="stack">`[-0, +0, -]`</span>

- `L`: Lua thread
- `tag`: Tag
- `dtor`: Tag


Assigns the destructor function for a given userdata tag. All userdata with the given tag will utilize this destructor during GC.

```cpp title="Example" hl_lines="17"
constexpr int kFooTag = 10;

struct Foo {
	char* some_allocated_data;
};

static void Foo_destructor(lua_State* L, void* data) {
	Foo* foo = static_cast<Foo*>(data);
	delete foo->some_allocated_data;
}

void setup_Foo(lua_State* L) {
	luaL_newmetatable(L, "Foo");
	// ...build metatable
	lua_setuserdatametatable(L, kFooTag);

	lua_setuserdatadtor(L, kFooTag, Foo_destructor);
}
```


----


### <span class="subsection">`lua_getuserdatadtor`</span>

<span class="signature">`lua_Destructor lua_getuserdatadtor(lua_State* L, int tag)`</span>
<span class="stack">`[-0, +0, -]`</span>

- `L`: Lua thread
- `tag`: Tag


Returns the destructor function assigned to the userdata tag.

```cpp title="Example" hl_lines="7 11"
constexpr int kFooTag = 10;
struct Foo {};
static void Foo_destructor(lua_State* L, void* data) {}

void setup_Foo(lua_State* L) {
	// ...
	auto dtor_before = lua_getuserdatadtor(L, kFooTag); // dtor_before == nullptr

	lua_setuserdatadtor(L, kFooTag, Foo_destructor);

	auto dtor_after = lua_getuserdatadtor(L, kFooTag); // dtor_after == Foo_destructor
}
```


----


### <span class="subsection">`lua_isuserdata`</span>

<span class="signature">`int lua_isuserdata(lua_State* L, int idx)`</span>
<span class="stack">`[-0, +0, -]`</span>

- `L`: Lua thread
- `idx`: Stack index


Returns `1` if the value at the given stack index is a userdata object. Otherwise, returns `0`.


----


### <span class="subsection">`luaL_checkudata`</span>

<span class="signature">`void* luaL_checkudata(lua_State* L, int ud, const char* name)`</span>
<span class="stack">`[0, +0, -]`</span>

- `L`: Lua thread
- `ud`: Userdata index
- `name`: Name


Asserts that a value on the stack is a userdata with a matching metatable to `name` (created with [`luaL_newmetatable`](#lual_newmetatable)).

```cpp title="Example" hl_lines="6"
constexpr const char* kFoo = "Foo";

struct Foo { /* ... */ };

Foo* check_Foo(lua_State* L, int idx) {
	return static_cast<Foo*>(luaL_checkudata(L, kFoo));
}
```


----


## Light Userdata Functions

### <span class="subsection">`lua_pushlightuserdata`</span>

<span class="signature">`void lua_pushlightuserdata(lua_State* L, void* p)`</span>
<span class="stack">`[-0, +1, -]`</span>

- `L`: Lua thread
- `p`: Pointer to arbitrary user-owned data


Pushes the tagged lightuserdata to the stack. Identical to `lua_pushlightuserdatatagged` with a tag of `0`.

```cpp title="Example" hl_lines="4"
struct Foo {};
Foo* foo = new Foo();

lua_pushlightuserdata(L, foo);
```


----


### <span class="subsection">`lua_pushlightuserdatatagged`</span>

<span class="signature">`void lua_pushlightuserdatatagged(lua_State* L, void* p, int tag)`</span>
<span class="stack">`[-0, +1, -]`</span>

- `L`: Lua thread
- `p`: Pointer to arbitrary user-owned data
- `tag`: Tag


Pushes the tagged lightuserdata to the stack. Use [`lua_tolightuserdatatagged`](#lua_tolightuserdatatagged) to retrieve the value. For more info on tags, see the [Tags](guide/tags.md) page.

```cpp title="Example" hl_lines="6"
constexpr int kFooTag = 1;
struct Foo {};

Foo* foo = new Foo();

lua_pushlightuserdatatagged(L, foo, kFooTag);
```


----


### <span class="subsection">`lua_tolightuserdata`</span>

<span class="signature">`void* lua_tolightuserdata(lua_State* L, int idx)`</span>
<span class="stack">`[-0, +0, -]`</span>

- `L`: Lua thread
- `idx`: Stack index


Returns a pointer to a lightuserdata on the stack. Returns `NULL` if the value is not a lightuserdata.

```cpp title="Example" hl_lines="10"
struct Foo {
	int n;
};

Foo* foo = new Foo();
foo->n = 32;

lua_pushlightuserdata(L, foo);

Foo* f = static_cast<Foo*>(lua_tolightuserdata(L, -1));
printf("foo->n = %d\n", foo->n); // foo->n = 32

// ...pop lightuserdata and delete allocation
```


----


### <span class="subsection">`lua_tolightuserdatatagged`</span>

<span class="signature">`void* lua_tolightuserdatatagged(lua_State* L, int idx, int tag)`</span>
<span class="stack">`[-0, +0, -]`</span>

- `L`: Lua thread
- `idx`: Stack index
- `tag`: Tag


Returns a pointer to a lightuserdata on the stack. Returns `NULL` if the value is not a lightuserdata _or_ if the attached tag does not equal the provided `tag` argument. For more info on tags, see the [Tags](guide/tags.md) page.

```cpp title="Example" hl_lines="12"
constexpr int kFooTag = 1;

struct Foo {
	int n;
};

Foo* foo = new Foo();
foo->n = 32;

lua_pushlightuserdatatagged(L, foo, kFooTag);

Foo* f = static_cast<Foo*>(lua_tolightuserdatatagged(L, -1, kFooTag));
printf("foo->n = %d\n", foo->n); // foo->n = 32

// ...pop lightuserdata and delete allocation
```


----


### <span class="subsection">`lua_islightuserdata`</span>

<span class="signature">`int lua_islightuserdata(lua_State* L, int idx)`</span>
<span class="stack">`[-0, +0, -]`</span>

- `L`: Lua thread
- `idx`: Stack index


Checks if the value at the given stack index is a lightuserdata.

```cpp title="Example"
if (lua_islightuserdata(L, -1)) { /* ... */ }
```


----


### <span class="subsection">`lua_lightuserdatatag`</span>

<span class="signature">`int lua_lightuserdatatag(lua_State* L, int idx)`</span>
<span class="stack">`[-0, +0, -]`</span>

- `L`: Lua thread
- `idx`: Stack index


Returns the tag for the lightuserdata at the given stack position. For non-lightuserdata values, this function returns `-1`. If the lightuserdata value was not assigned a tag, the tag will be set to the default of `0`, and thus this function will return `0`.

```cpp title="Example" hl_lines="17-19"
constexpr int kFooTag = 10;
constexpr int kBarTag = 20;

struct Foo {};
struct Bar {};
struct Baz {};

Foo* foo = new Foo();
lua_pushlightuserdatatagged(L, foo, kFooTag);

Bar* bar = new Bar();
lua_pushlightuserdatatagged(L, bar, kBarTag);

Baz* baz = new Baz();
lua_pushlightuserdata(L, baz);

int foo_tag = lua_lightuserdatatag(L, -3); // 10
int bar_tag = lua_lightuserdatatag(L, -2); // 20
int baz_tag = lua_lightuserdatatag(L, -1); // 0

// ...pop lightuserdata and delete allocations
```


----


### <span class="subsection">`lua_setlightuserdataname`</span>

<span class="signature">`void lua_setlightuserdataname(lua_State* L, int tag, const char* name)`</span>
<span class="stack">`[-0, +0, -]`</span>

- `L`: Lua thread
- `tag`: Tag
- `name`: Name


Sets the name for the tagged lightuserdata. The string is copied, so the provided name argument is safe to dispose.

Calling this function more than once for the same tag will throw an error.

```cpp title="Example"
constexpr int kMyDataTag = 10;
lua_setlightuserdataname(L, kMyDataTag, "MyData");
```


----


### <span class="subsection">`lua_getlightuserdataname`</span>

<span class="signature">`const char* lua_getlightuserdataname(lua_State* L, int tag)`</span>
<span class="stack">`[-0, +0, -]`</span>

- `L`: Lua thread
- `tag`: Tag


Returns the name for the tagged lightuserdata (or `nullptr` if no name is assigned).

```cpp title="Example" hl_lines="3"
constexpr int kMyDataTag = 10;
lua_setlightuserdataname(L, kMyDataTag, "MyData");
const char* name = lua_getlightuserdataname(L, kMyDataTag); // name == "MyData"
```


----


## Load and Call Functions

### <span class="subsection">`luau_load`</span>

<span class="signature">`int luau_load(lua_State* L, const char* chunkname, const char* data, size_t size, int env)`</span>
<span class="stack">`[-0, +1, -]`</span>

- `L`: Lua thread
- `chunkname`: Chunk name
- `data`: Bytecode data
- `size`: Bytecode data size
- `env`: Environment


Loads bytecode onto the given thread as a callable function on the top of the stack. If loading fails, the error message is pushed to the stack instead.

The `chunkname` argument helps with debugging.

Set `env` to `0` to use the default environment. Otherwise, this indicates the stack index for the given environment to use.

```cpp title="Example" hl_lines="6"
const char* source = "print('hello')";

size_t bytecode_size;
char* bytecode = luau_compile(source, strlen(source), nullptr, &bytecode_size);

int res = luau_load(L, "=test", bytecode, bytecode_size, 0);
free(bytecode);

if (res != 0) {
	size_t len;
	const char* msg = lua_tolstring(L, -1, &len);
	lua_pop(L, 1);
	printf("failed to compile: %s\n", msg);
	return;
}

// Move loaded chunk to its own thread and run it:
lua_State* T = lua_newthread(L);
lua_pushvalue(L, -2);
lua_remove(L, -3);
lua_xmove(L, T, 1);
int status = lua_resume(T, nullptr, 0);
// ...handle status
```


----


### <span class="subsection">`lua_call`</span>

<span class="signature">`void lua_call(lua_State* L, int nargs, int nresults)`</span>
<span class="stack">`[-(nargs + 1), +nresults, -]`</span>

- `L`: Lua thread
- `nargs`: Number of arguments
- `nresults`: Number of returned values


Calls the function at the top of the stack with `nargs` arguments, and expecting `nresults` return values. To use `lua_call`, push the desired function to the stack, and then push the desired arguments to the stack next.

If the function errors, the program will need to handle the error. This differs based on how Luau was built. See [Error Handling](guide/error-handling.md) for more information. Also consider using [`lua_pcall`](#lua_pcall) instead.

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


----


### <span class="subsection">`lua_pcall`</span>

<span class="signature">`void lua_pcall(lua_State* L, int nargs, int nresults, int errfunc)`</span>
<span class="stack">`[-(nargs + 1), +nresults, -]`</span>

- `L`: Lua thread
- `nargs`: Number of arguments
- `nresults`: Number of returned values
- `errfunc`: Error function index (or 0 for none)


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


----


### <span class="subsection">`lua_cpcall`</span>

<span class="signature">`int lua_cpcall(lua_State* L, lua_CFunction func, void* ud)`</span>
<span class="stack">`[-(nargs + 1), +nresults, -]`</span>

- `L`: Lua thread
- `func`: C function
- `ud`: Light userdata


Calls the C function in protected mode, passing `ud` as the single item on the stack for the function. Returns the status, just like `lua_pcall`. Functions returned by `func` are automatically discarded.

```cpp title="Example" hl_lines="13"
struct Foo {
	int n;
};

int fn(lua_State* L) {
	Foo* foo = static_cast<Foo*>(lua_tolightuserdata(L, 1));
	foo->n *= 2;
	return 0;
}

Foo foo{};
foo.n = 10;
int status = lua_cpcall(L, fn, &foo);

if (status == LUA_OK) {
	printf("n: %d\n", foo.n); // n: 20
} else {
	const char* err = lua_tostring(L, -1);
	lua_pop(L, 1);
	printf("error: %s\n", err);
}
```


----


### <span class="subsection">`luaL_callyieldable`</span>

<span class="signature">`int luaL_callyieldable(lua_State* L, int nargs, int nresults)`</span>
<span class="stack">`[-(nargs + 1), +nresults, -]`</span>

- `L`: Lua thread
- `nargs`: Number of arguments
- `nresults`: Number of returned values


Similar to `lua_call`, except this function can call yieldable C functions.

Returns the status of the call. If the call was a C function and the C function yielded, this will be `-1`.


----


## Load and Call Functions

### <span class="subsection">`lua_yield`</span>

<span class="signature">`void lua_yield(lua_State* L, int nresults)`</span>
<span class="stack">`[-?, +?, -]`</span>

- `L`: Lua thread
- `nresults`: Number of returned values


Yields a coroutine thread. This should only be called as the return value of a C function.

The `nresults` argument indicates how many stack values remain on the thread's stack, allowing the caller of `lua_resume` to grab those values.

```cpp title="Example"
int do_something(lua_State* L) {
	// Yield back '15' to the lua_resume call:
	lua_pushinteger(L, 15);
	return lua_yield(L, 1);
}

lua_State* T = lua_newthread(L);
lua_pushcfunction(T, do_something, "do_something");
int status = lua_resume(L, 0);
if (status == LUA_YIELD) {
  int value = lua_tointeger(T, 1); // 15
  lua_pop(T, 1);
}
```


----


### <span class="subsection">`lua_break`</span>

<span class="signature">`void lua_break(lua_State* L)`</span>
<span class="stack">`[-0, +0, -]`</span>

- `L`: Lua thread


Trigger a break (i.e. breakpoint). This is different than `lua_breakpoint`, which installs a breakpoint.


----


### <span class="subsection">`lua_resume`</span>

<span class="signature">`int lua_resume(lua_State* L, lua_State* from, int narg)`</span>
<span class="stack">`[-?, +?, -]`</span>

- `L`: Lua thread
- `from`: From Lua thread
- `narg`: Number of arguments


Resumes a coroutine. The status of the resumption is returned.

To start a new coroutine, do the following:
1. Create a new thread, e.g. [`lua_newthread`](#lua_newthread)
1. Place a function onto the new thread's stack
1. Place arguments in-order onto the new thread's stack (same amount as indicated with `narg` argument)
1. Call `lua_resume`
1. Handle the result

To resume an existing coroutine:
1. Place arguments onto the thread's stack (These will be the returned result from Luau's `coroutine.yield` call)
1. Call `lua_resume`
1. Handle the result

```cpp title="Example" hl_lines="22"
int add(lua_State* L) {
	// Get args:
	int a = luaL_checkinteger(L, 1);
	int b = luaL_checkinteger(L, 2);

	lua_pushinteger(L, a + b);

	return 1;
}

// Create thread:
lua_State* T = lua_newthread(L);

// Push function to thread:
lua_pushcfunction(add, "add");

// Push arguments:
lua_pushinteger(T, 10);
lua_pushinteger(T, 20);

// Resume:
int status = lua_resume(T, L, 2);

if (status == LUA_OK) {
	// Coroutine is done
	printf("ok");
} else if (status == LUA_YIELD) {
	// Handle yielded thread
	printf("yielded");
} else {
	// Handle error (call lua_getinfo and lua_debugtrace for better debugging and stacktrace information)
	if (const char* str = lua_tostring(T, -1)) {
		printf("error: %s\n", str);
	} else {
		printf("unknown error: %d\n", status);
	}
}
```


----


### <span class="subsection">`lua_resumeerror`</span>

<span class="signature">`int lua_resumeerror(lua_State* L, lua_State* from)`</span>
<span class="stack">`[-?, +?, -]`</span>

- `L`: Lua thread
- `from`: From Lua thread


Resumes a coroutine, but in an error state. This is useful when reporting an error to a yielded thread.

For example, a coroutine might yield to wait for some sort of web request. The yielded thread needs to be resumed, but also needs to report that an error occurred. Thus, `lua_resume` would not be adequate.

The status of the resumption is returned.

```cpp title="Example" hl_lines="8"
// Some sort of error occurs for our thread, e.g. a web request fails
// We'll push a string onto the stack to indicate what went wrong
lua_pushliteral(T, "oh no, the request failed!");

// Elsewhere, in some hypothetical task scheduler, we resume the yielded thread:
int status;
if (there_was_an_error) {
	status = lua_resumeerror(T, L);
} else {
	// ...normal resumption
}

// ...handle status
if (status != LUA_OK && status != LUA_YIELD) {
	const char* err = lua_tostring(T, -1); // Might be our "oh no, the request failed!" error message
	// ...other more complete error handling
}
```


----


### <span class="subsection">`lua_status`</span>

<span class="signature">`int lua_status(lua_State* L)`</span>
<span class="stack">`[-0, +0, -]`</span>

- `L`: Lua thread


Returns any `lua_Status` value:
```cpp title="lua_Status"
// Copied from luau/VM/include/lua.h
enum lua_Status {
	  LUA_OK = 0,
    LUA_YIELD,
    LUA_ERRRUN,
    LUA_ERRSYNTAX, // legacy error code, preserved for compatibility
    LUA_ERRMEM,
    LUA_ERRERR,
    LUA_BREAK, // yielded for a debug breakpoint
};
```

```cpp title="Example" hl_lines="15 19 23"
int all_good(lua_State* L) {
	return 0;
}

int oh_no(lua_State* L) {
	luaL_error("oh no!");
}

int yield_something(lua_State* L) {
	return lua_yield(L, 0);
}

lua_State* T = lua_newthread(L);
lua_pushcfunction(all_good, "all_good");
int status = lua_resume(T, nullptr, 0); // LUA_OK (0)

lua_State* T = lua_newthread(L);
lua_pushcfunction(oh_no, "oh_no");
int status = lua_resume(T, nullptr, 0); // LUA_ERRRUN (2)

lua_State* T = lua_newthread(L);
lua_pushcfunction(yield_something, "yield_something");
int status = lua_resume(T, nullptr, 0); // LUA_YIELD (1)
```


----


### <span class="subsection">`lua_isyieldable`</span>

<span class="signature">`int lua_isyieldable(lua_State* L)`</span>
<span class="stack">`[-0, +0, -]`</span>

- `L`: Lua thread


Returns `1` if the coroutine is yieldable, otherwise `0`.


----


### <span class="subsection">`lua_getthreaddata`</span>

<span class="signature">`void* lua_getthreaddata(lua_State* L)`</span>
<span class="stack">`[-0, +0, -]`</span>

- `L`: Lua thread


Gets data attached to the given thread. This is arbitrary data that is assigned with [`lua_setthreaddata`](#lua_setthreaddata).


----


### <span class="subsection">`lua_setthreaddata`</span>

<span class="signature">`void lua_setthreaddata(lua_State* L)`</span>
<span class="stack">`[-0, +0, -]`</span>

- `L`: Lua thread


Sets arbitrary data for a given thread. This is often useful when using lua interrupt or thread callbacks (see [`lua_callbacks`](#lua_callbacks)).

This value ought not be a Luau-owned object (e.g. data created with `lua_newuserdata`), since the lifetime of that memory may be shorter than the lifetime of the given thread.

```cpp title="Example"
class Foo {};

lua_setthreaddata(L, new Foo());
// ...
Foo* foo = static_cast<Foo*>(lua_getthreaddata(L));
// ...
lua_setthreaddata(L, nullptr);
delete foo;
```


----


### <span class="subsection">`lua_costatus`</span>

<span class="signature">`int lua_costatus(lua_State* L)`</span>
<span class="stack">`[-0, +0, -]`</span>

- `L`: Lua thread


Gets the coroutine status (`lua_CoStatus`) of a given thread.

```cpp title="lua_CoStatus"
// Copied from luau/VM/include/lua.h
enum lua_CoStatus {
    LUA_CORUN = 0, // running
    LUA_COSUS,     // suspended
    LUA_CONOR,     // 'normal' (it resumed another coroutine)
    LUA_COFIN,     // finished
    LUA_COERR,     // finished with error
};
```


----


## Memory Functions

### <span class="subsection">`lua_gc`</span>

<span class="signature">`int lua_gc(lua_State* L, int what, int data)`</span>
<span class="stack">`[-0, +0, -]`</span>

- `L`: Lua thread
- `what`: What
- `data`: Data


Various garbage collection operations, determined by the `what` argument.

Starting and stopping the GC:

- To stop the GC: `lua_gc(L, LUA_GCSTOP, 0);`
- To restart the GC: `lua_gc(L, LUA_GCRESTART, 0);`
- To run a full GC cycle: `lua_gc(L, LUA_GCCOLLECT, 0);`
- To run a GC step: `lua_gc(L, LUA_GCSTEP, 0);`

Querying the GC:

- To check if the GC is running: `if (lua_gc(L, LUA_GCISRUNNING, 0)) {}`
- To count GC usage in kilobytes: `int kb = lua_gc(L, LUA_GCCOUNT, 0);`
- To count the remaining GC in bytes: `int b = lua_gc(L, LUA_GCCOUNTB, 0);`

Tuning the GC:

- To set the GC goal (percentage): `lua_gc(L, LUA_GCSETGOAL, 200);`
- To set the GC step multiplier (percentage): `lua_gc(L, LUA_GCSETSTEPMUL, 200);`
- To set the GC step size (KB): `lua_gc(L, LUA_GCSETSTEPSIZE, 1);`

```cpp title="Example"
// Example of querying bytes used:
int kb = lua_gc(L, LUA_GCCOUNT, 0);
int bytes_remaining = lua_gc(L, LUA_GCCOUNTB, 0);
int bytes_total = (kb * 1024) + byte_remaining;
printf("gc size: %d bytes", bytes_total);
```


----


### <span class="subsection">`lua_setmemcat`</span>

<span class="signature">`int lua_setmemcat(lua_State* L, int category)`</span>
<span class="stack">`[-0, +0, -]`</span>

- `L`: Lua thread
- `category`: Memory category


Set the memory category for a given thread (the default is `0`). There is no associated function to retrieve a thread's current memory category.

Call [`lua_totalbytes`](#lua_totalbytes) to query the amount of memory utilized by a given memory category.

**Note:** While the `category` parameter is an `int`, the actual memory category attached to the thread is a `uint8_t`, and thus the category parameter is cast to `uint8_t`. Therefore, memory categories are limited to the range `[0, 255]`.

```cpp title="Example"
// Set the memory category of `L` to 10:
lua_setmemcat(L, 10);
```


----


### <span class="subsection">`lua_totalbytes`</span>

<span class="signature">`size_t lua_totalbytes(lua_State* L, int category)`</span>
<span class="stack">`[-0, +0, -]`</span>

- `L`: Lua thread
- `category`: Memory category


Retrieves the total bytes allocated by a given memory category (`0` is the default memory category). Call [`lua_setmemcat`](#lua_setmemcat) to assign a memory category for a given thread.

```cpp title="Example" hl_lines="7"
constexpr uint8_t kExampleMemCat = 10;

lua_State* T = lua_newthread(L);
lua_setmemcat(T, kExampleMemCat);
lua_newbuffer(T, 1024 * 10); // 10KB buffer

size_t total_bytes = lua_totalbytes(T, kExampleMemCat);
printf("total: %zu bytes\n", total_bytes);
```


----


## Error Functions

### <span class="subsection">`lua_error`</span>

<span class="signature">`l_noret lua_error(lua_State* L)`</span>
<span class="stack">`[-0, +0, -]`</span>

- `L`: Lua thread


Throws a Luau error. Expects the error message to be on the top of the stack. Depending on how Luau is built, this will either perform a `longjmp` or throw a C++ `luau_exception`. See [Error Handling](guide/error-handling.md) for more information.

Using [`luaL_error`](#lual_error) is typically a more ergonomic way to throw errors, since an error message can be provided.

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


----


### <span class="subsection">`luaL_error`</span>

<span class="signature">`l_noret luaL_error(lua_State* L, const char* fmt,  ...)`</span>
<span class="stack">`[-0, +0, -]`</span>

- `L`: Lua thread
- `fmt`: Format string
- `...`: Args


Throws a Luau error with the given error message.

```cpp title="Example"
luaL_error(L, "something went wrong");

// Error message can be formatted:
int some_code = 2;
const char* message = "it zigged but it should have zagged";
luaL_error(L, "%d - %s", some_code, message);
```


----


### <span class="subsection">`luaL_typeerror`</span>

<span class="signature">`l_noret luaL_typeerror(lua_State* L, int narg, const char* tname)`</span>
<span class="stack">`[-0, +0, -]`</span>

- `L`: Lua thread
- `narg`: Argument number
- `tname`: Type name


Throws a Luau error with a templated error message for an incorrect type.

```cpp title="Example"
int send_table(lua_State* L) {
	// expects a table as the first argument
	if (!lua_istable(L, 1)) {
		luaL_typeerror(L, 1, "table"); // "invalid argument #1 to 'send_table' (table expected, got <TYPENAME>)"
	}

	// ...
}
```


----


### <span class="subsection">`luaL_argexpected`</span>

<span class="signature">`l_noret luaL_argexpected(lua_State* L, int cond, int narg, const char* tname)`</span>
<span class="stack">`[-0, +0, -]`</span>

- `L`: Lua thread
- `cond`: Condition
- `narg`: Argument number
- `tname`: Type name


Throws a Luau error with a templated error message for an incorrect type. This is similar to `luaL_typeerror`, except it encapsulates a condition, similar to an assertion.

```cpp title="Example"
int send_table(lua_State* L) {
	// expects a table as the first argument
	luaL_argexpected(L, lua_istable(L, 1), 1, "table");

	// ...
}
```


----


### <span class="subsection">`luaL_argerror`</span>

<span class="signature">`l_noret luaL_argerror(lua_State* L, int narg, const char* extramsg)`</span>
<span class="stack">`[-0, +0, -]`</span>

- `L`: Lua thread
- `narg`: Argument number
- `extramsg`: Extra message


Throws a Luau error with a templated error message for an incorrect argument.

```cpp title="Example" hl_lines="5-7"
int divide(lua_State* L) {
	double numerator = luaL_checknumber(L, 1);
	double denominator = luaL_checknumber(L, 2);

	if (denominator == 0) {
		luaL_argerror(L, 2, "cannot divide by zero");
	}

	lua_pushnumber(L, numerator / denominator);
	return 1;
}
```


----


### <span class="subsection">`luaL_argcheck`</span>

<span class="signature">`l_noret luaL_argcheck(lua_State* L, int cond, int narg, const char* extramsg)`</span>
<span class="stack">`[-0, +0, -]`</span>

- `L`: Lua thread
- `cond`: Condition
- `narg`: Argument number
- `extramsg`: Extra message


Throws a Luau error with a templated error message for an incorrect argument. This is similar to `luaL_argerror`, except it encapsulates a condition, similar to an assertion.

```cpp title="Example" hl_lines="5"
int divide(lua_State* L) {
	double numerator = luaL_checknumber(L, 1);
	double denominator = luaL_checknumber(L, 2);

	luaL_argcheck(L, denominator == 0, 2, "cannot divide by zero");

	lua_pushnumber(L, numerator / denominator);
	return 1;
}
```


----


## Miscellaneous Functions

### <span class="subsection">`lua_next`</span>

<span class="signature">`int lua_next(lua_State* L, int idx)`</span>
<span class="stack">`[-1, +(2|0), -]`</span>

- `L`: Lua thread
- `idx`: Stack index


The `lua_next` function is used to get the next key/pair value in a table, and thus is typically used to iterate a table. Note that [`lua_rawiter`](#lua_rawiter) is a faster and preferable way of iterating a table.

This function pops a key from the top of the stack and pushes two values: the next key and value in the table. The table is located at the provided `idx` position on the stack. If there are no more items next within the table, then nothing is pushed to the stack and the function returns `0`.

To get the first key/value pair in a table, use `nil` as the first key.

```cpp title="Example" hl_lines="4"
// Assume a table is at the top of the stack

lua_pushnil(L); // First key is nil to indicate we want the first key/value pair from the table
while (lua_next(L, -2) != 0) { // -2 is the stack index for the table
	// Key is now at index -2
	// Value is now at index -1
	printf("%s: %s\n", luaL_typename(L, -2), luaL_typename(L, -1));

	// Remove 'Value' from the stack, leaving only the Key, which is used
	// within the next iteration of the loop, and thus is fed back into
	// the lua_next function.
	lua_pop(L, 1);
}

// Nothing to clean up here, as lua_next consumed the keys given. If we happened
// to break out of the loop early, we would need to pop the key/value items.

// In this example, the table is once again at the top of the stack here.
```

The `lua_next` function can also be used to check if a Luau table is empty. Luau tables can be both arrays and dictionaries, but the `lua_objlen` function will only count the size of the array portion of the table. Thus, `lua_objlen` might return `0` even if the dictionary portion of the array has items. If given a `nil` key, `lua_next` will only return `0` if both the array and dictionary portion of the table are empty.

```cpp title="Empty Example"
bool is_table_empty(lua_State* L, int idx) {
	// User may provide a negative index to the desired table, but we need
	// to manipulate the stack, so we can use lua_absindex to get the absolute
	// index of the table, which will remain stable as we change the stack:
	int abs_idx = lua_absindex(L, idx);

	lua_pushnil(L);
	if (lua_next(L, abs_idx)) {
		lua_pop(L, 2); // Pop the key/value pair produced by lua_next
		return true;
	}

	return false;
}
```


----


### <span class="subsection">`lua_rawiter`</span>

<span class="signature">`int lua_rawiter(lua_State* L, int idx, int iter)`</span>
<span class="stack">`[-0, +2, -]`</span>

- `L`: Lua thread
- `idx`: Stack index
- `iter`: Iterator


Allows for iterating over a Luau table. This iterates over both the array and dictionary portions of the table. The `idx` argument is the stack index of the table. The `iter` argument is the previous index provided by `lua_rawiter` (or `0` for the initial call). See the example below to see how to use this function within a standard for-loop.

The current implementation will iterate over the array portion first, followed by the dictionary portion. However, implementation details are not reliable, and any code should not assume this order will always be the same.

**Note:** The returned value of `lua_rawiter` cannot be used to index directly into the table itself (e.g. `lua_rawgeti`). Instead, the `lua_rawiter` function will push the key/value pair onto the stack. These values should both be popped before iterating again.

```cpp title="Example"
// Assume a table is at the top of the stack

// Note the somewhat different for-loop setup, assigning and checking the index
// within the condition check of the loop, and no update expression is used:
for (int index = 0; index = lua_rawiter(L, -1, index), index >= 0;) {
	// Key is at stack index -2
	// Value is at stack index -1
	printf("%s:%s\n", luaL_typename(L, -2), luaL_typename(L, -1));
	lua_pop(L, 2); // Pop the key and value
}
```


----


### <span class="subsection">`lua_concat`</span>

<span class="signature">`void lua_concat(lua_State* L, int n)`</span>
<span class="stack">`[-n, +1, -]`</span>

- `L`: Lua thread
- `n`: Number of values


Performs string concatenation on the `n` values on the top of the stack. All `n` values are popped, and the resultant string is pushed to the stack. If `n` is `1`, this function does nothing. If `n` is `0`, an empty string is pushed to the stack. For all other values of `n` (assuming >= 2), all values are popped and concatenated into a string.


----


### <span class="subsection">`lua_encodepointer`</span>

<span class="signature">`uintptr_t lua_encodepointer(lua_State* L, uintptr_t p)`</span>
<span class="stack">`[-0, +0, -]`</span>

- `L`: Lua thread
- `p`: Pointer


Encodes a pointer.

```cpp title="Example" hl_lines="3"
lua_newtable(L);
const void* ptr = lua_topointer(L, -1);
uintptr_t encoded_ptr = lua_encodepointer(L, uintptr_t(ptr));
printf("Pointer: 0x%016llx\n", encoded_ptr);
```


----


### <span class="subsection">`lua_clock`</span>

<span class="signature">`double lua_clock()`</span>
<span class="stack">`[-0, +0, -]`</span>


Returns high-precision timestamp in seconds from the OS. This is exactly what the Luau library function `os.clock` uses. Here is the OS Clock function implementation:

```cpp title="example" hl_lines="3"
// Copied from luau/VM/src/loslib.cpp
static int os_clock(lua_State* L) {
	lua_pushnumber(L, lua_clock());
	return 1;
}
```


----


### <span class="subsection">`lua_clonefunction`</span>

<span class="signature">`void lua_clonefunction(lua_State* L, int idx)`</span>
<span class="stack">`[-0, +1, -]`</span>

- `L`: Lua thread
- `idx`: Stack index


Clones a Luau function at the given index and pushes the cloned function to the top of the stack.


----


### <span class="subsection">`lua_cleartable`</span>

<span class="signature">`void lua_cleartable(lua_State* L, int idx)`</span>
<span class="stack">`[-0, +0, -]`</span>

- `L`: Lua thread
- `idx`: Stack index


Clears the table at the given index. The internal table capacity does not shrink by default (tables can be configured to shrink by setting `__mode = "s"` on a table's metatable, but only do this if necessary).

```cpp title="Example" hl_lines="10"
// Create a table with 10 numbers:
lua_newtable(L);
for (int i = 1; i <= 10; i++) {
	lua_pushinteger(L, i);
	lua_rawseti(L, -2, i); // t[i] = i
}

printf("Length: %d\n", lua_objlen(L, -1)); // Length: 10

lua_cleartable(L, -1);

printf("Length: %d\n", lua_objlen(L, -1)); // Length: 0
```


----


### <span class="subsection">`lua_clonetable`</span>

<span class="signature">`void lua_clonetable(lua_State* L, int idx)`</span>
<span class="stack">`[-0, +1, -]`</span>

- `L`: Lua thread
- `idx`: Stack index


Creates a shallow copy of the table at `idx` on the stack. The copied table is pushed to the stack.

```cpp title="Example" hl_lines="9"
// Create a table with 10 numbers:
lua_newtable(L);
for (int i = 1; i <= 10; i++) {
	lua_pushinteger(L, i);
	lua_rawseti(L, -2, i); // t[i] = i
}

// Clone the table:
lua_clonetable(L, -1);

// Clear the original table:
lua_cleartable(L, -2);

// Show that they have different lengths:
printf("Length Original: %d\n", lua_objlen(L, -2)); // Length Original: 0
printf("Length Clone: %d\n", lua_objlen(L, -1)); // Length Clone: 10
```


----


### <span class="subsection">`lua_getallocf`</span>

<span class="signature">`lua_Alloc lua_getallocf(lua_State* L, void** ud)`</span>
<span class="stack">`[-0, +0, -]`</span>

- `L`: Lua thread
- `ud`: Userdata


Returns the memory allocator function, and writes the the opaque userdata pointer. These are the values that were originally passed to `lua_newstate`.

**Note:** `ud` is only written if the value was provided as non-null to `lua_newstate`. Beware of garbage values.

```cpp title="Example"
void* ud = nullptr; // Note: explicitly initalized as nullptr
lua_Alloc alloc_fn = lua_getallocf(L, &ud);
```


----


### <span class="subsection">`lua_callbacks`</span>

<span class="signature">`lua_Callbacks* lua_callbacks(lua_State* L)`</span>
<span class="stack">`[-0, +0, -]`</span>

- `L`: Lua thread


Allows users to install callback functions for various purposes.

```cpp title="Example"
// Handle Luau panics (only when Luau is built with longjmp, not C++ exceptions)
static void handle_panic(lua_State* L, int errcode) {
	fprintf(stderr, "luau panic: %d\n", errcode);
}

// Called when thread 'L' is created or destroyed, denoted if LP (L parent) exists or is null
static void handle_user_thread(lua_State* LP, lua_State* L) {
	if (LP == nullptr) {
		// L was destroyed
	} else {
		// L was created
	}
}

lua_callbacks(L)->panic = handle_panic;
lua_callbacks(L)->userthread = handle_user_thread;
// ...
```


----


### <span class="subsection">`luaL_findtable`</span>

<span class="signature">`const char* luaL_findtable(lua_State* L, int idx, const char* fname, int szhint)`</span>
<span class="stack">`[-0, +1, -]`</span>

- `L`: Lua thread
- `idx`: Stack index
- `fname`: Name
- `szhint`: Size hint


Attempts to find or create a table within the table at `idx`. Using dot-notation within `fname`, this can be a nested table. The `szhint` argument indicates how many slots should be allocated in the dictionary portion of the table (if a new table is created).

If there is a name conflict (i.e. a value exists with the provided name, but it isn't a table), then said name is returned. Otherwise, `NULL` is returned.

```cpp title="Example"
// Pushes the table "my_data" under the Luau registry to the stack.
// If the table doesn't exist yet, it is created.
luaL_findtable(L, LUA_REGISTRYINDEX, "my_data", 1);

// Finds table "another" within the hierarchy (and creates each parent table as needed)
luaL_findtable(L, LUA_REGISTRYINDEX, "mydata.subtable.another", 1);

// Same as above, except "my_data" is sourced from the new table provided.
lua_newtable(L);
luaL_findtable(L, -1, "my_data", 1);
lua_pushliteral(L, "hello");
lua_rawsetfield(L, "message", -2); // mydata.message = "hello"

// Conflicts are returned ("hello" exists within "my_data" but isn't a table):
const char* conflict = luaL_findtable(L, -1, "my_data.hello.nested");
if (conflict) {
	printf("name conflict: %s\n", conflict) // "name conflict: hello"
}
```


----


### <span class="subsection">`luaL_checktype`</span>

<span class="signature">`void luaL_checktype(lua_State* L, int narg, int t)`</span>
<span class="stack">`[-0, +0, m]`</span>

- `L`: Lua thread
- `narg`: Argument number
- `t`: Luau type


Asserts the type at the given index.

```cpp title="Example"
int do_something(lua_State* L) {
	// Assert that the first argument is a table:
	luaL_checktype(L, 1, LUA_TTABLE);
}
```


----


### <span class="subsection">`luaL_checkoption`</span>

<span class="signature">`int luaL_checkoption(lua_State* L, int idx, const char* def, const char* const lst[])`</span>
<span class="stack">`[-0, +0, -]`</span>

- `L`: Lua thread
- `idx`: Stack index
- `def`: Default option
- `lst[]`: Options list


Asserts the value at the given index is a string within the given options list `lst`. If `def` is provided (non-null), then `def` will be used as the default option if the value at the given stack index is nil or none. If the assertion passes, the index to the item in the list is returned.

```cpp title="Example"
int set_mode(lua_State* L) {
	static const char* const options[] = {"follow", "defend", "attack", "flee", nullptr};

	int i = luaL_checkoption(L, 1, options[0], options);
	const char* option = options[i];
	// ...
}
```


----


### <span class="subsection">`luaL_checkany`</span>

<span class="signature">`void luaL_checkany(lua_State* L, int narg)`</span>
<span class="stack">`[-0, +0, m]`</span>

- `L`: Lua thread
- `narg`: Argument number


Asserts the value at the given index is any value (including `nil`). In other words, this asserts that the value is not none.


----


### <span class="subsection">`luaL_register`</span>

<span class="signature">`int luaL_register(lua_State* L, const char* libname, const luaL_Reg* l)`</span>
<span class="stack">`[-0, +(0|1), -]`</span>

- `L`: Lua thread
- `libname`: Library name
- `l`: Functions


Registers a library (i.e. a collection of functions within their own namespace). Internally, this is just a table of functions mapped by their associated key from `l`.

If `libname` is not null, the library is placed in the Luau registry and the new library table is pushed to the stack. Any Luau code will be able to access the library by name.

If `libname` is null, the function assumes a table is at the top of the stack, and will register all functions into that table.

```cpp title="Example" hl_lines="6-11 14"
// Library functions:
static int do_this(lua_State* L) { /* ... */ }
static int do_that(lua_State* L) { /* ... */ }

// Define library key/pairs:
static const luaL_Reg foo_lib[] = {
	// {Name, C Function}
	{"dothis", do_this},
	{"dothat", do_that},
	{nullptr, nullptr}, // End of list is denoted by null pair
};

void open_foo(lua_State* L) {
	luaL_register(L, "foo", foo_lib);
	lua_pop(L, 1); // luaL_register had left our library on the stack
}
```

```luau title="Luau Example"
-- Luau can now access "foo":
foo.dothis()
foo.dothat()
```

Alternatively, `luaL_register` can be used to write the functions to an already-existing table. For instance, a metatable:
```cpp title="Example Metatable" hl_lines="9-14 18"
constexpr int kFooTag = 10;

struct Foo {};

static int Foo_index(lua_State* L) { /* ... */ }
static int Foo_newindex(lua_State* L) { /* ... */ }
static int Foo_tostring(lua_State* L) { /* ... */ }

static const luaL_Reg foo_mt[] = {
	{"__index", Foo_index},
	{"__newindex", Foo_newindex},
	{"__tostring", Foo_tostring},
	{nullptr, nullptr},
};

void Foo_setup_metatable(lua_State* L) {
	luaL_newmetatable(L, "Foo");
	luaL_register(L, nullptr, foo_mt);
	lua_setuserdatametatable(L, kFooTag);
}
```


----


## Ref Functions

### <span class="subsection">`lua_ref`</span>

<span class="signature">`int lua_ref(lua_State* L, int idx)`</span>
<span class="stack">`[-0, +0, -]`</span>

- `L`: Lua thread
- `idx`: Stack index


Creates a reference to the given Luau value at `idx` on the stack. The returned integer can be seen as an opaque handle to the value. Creating a reference is also an easy way to pin a Luau value, preventing it from being GC'd. A reference can be created for any value on the stack. Attempting to create a reference to a nil value will return `LUA_REFNIL`.

Be sure to call [`lua_unref`](#lua_unref) when done with the reference. Call [`lua_getref`](#lua_getref) to retrieve the referenced value.

**Note:** Unlike in Lua, Luau does _not_ modify the stack when creating a reference. The stack remains the same.

```cpp title="Example" hl_lines="2"
lua_newtable(L);
int table_ref = lua_ref(L, -1);
lua_pop(L, 1);
// GC won't clean up the table, even though it was popped, becase a reference
// has been created for the table.
```


----


### <span class="subsection">`lua_unref`</span>

<span class="signature">`void lua_unref(lua_State* L, int ref)`</span>
<span class="stack">`[-0, +0, -]`</span>

- `L`: Lua thread
- `ref`: Reference


Removes a reference that was originally created with `lua_ref`. Passing in `LUA_REFNIL` or `LUA_NOREF` is allowed (in those cases, the function does nothing). However, passing in an already-removed reference is _not_ allowed and may throw an error, or silently remove another reference. If idempotence is required, ensure your reference variable is set to `LUA_REFNIL` or `LUA_NOREF` after calling `lua_unref`.

```cpp title="Example" hl_lines="5"
lua_newtable(L);
int table_ref = lua_ref(L, -1);

// Sometime later:
lua_unref(L, table_ref);
```


----


### <span class="subsection">`lua_getref`</span>

<span class="signature">`int lua_getref(lua_State* L, int ref)`</span>
<span class="stack">`[-0, +1, -]`</span>

- `L`: Lua thread
- `ref`: Reference


Retrieves the value from a given reference handle. The value is pushed to the top of the stack.

```cpp title="Example" hl_lines="5"
lua_newtable(L);
int table_ref = lua_ref(L, -1);

// Sometime later:
lua_getref(L, table_ref);
// Top of stack is now the table from the reference
```


----


## Type Functions

### <span class="subsection">`lua_isfunction`</span>

<span class="signature">`int lua_isfunction(lua_State* L, int idx)`</span>
<span class="stack">`[-0, +0, -]`</span>

- `L`: Lua thread
- `idx`: Stack index


Checks if the value at the given stack index is a function.

```cpp title="Example"
if (lua_isfunction(L, -1)) { /* ... */ }
```


----


### <span class="subsection">`lua_istable`</span>

<span class="signature">`int lua_istable(lua_State* L, int idx)`</span>
<span class="stack">`[-0, +0, -]`</span>

- `L`: Lua thread
- `idx`: Stack index


Checks if the value at the given stack index is a table.

```cpp title="Example"
if (lua_istable(L, -1)) { /* ... */ }
```


----


### <span class="subsection">`lua_isnil`</span>

<span class="signature">`int lua_isnil(lua_State* L, int idx)`</span>
<span class="stack">`[-0, +0, -]`</span>

- `L`: Lua thread
- `idx`: Stack index


Checks if the value at the given stack index is nil.

```cpp title="Example"
if (lua_isnil(L, -1)) { /* ... */ }
```


----


### <span class="subsection">`lua_isthread`</span>

<span class="signature">`int lua_isthread(lua_State* L, int idx)`</span>
<span class="stack">`[-0, +0, -]`</span>

- `L`: Lua thread
- `idx`: Stack index


Checks if the value at the given stack index is a thread.

```cpp title="Example"
if (lua_isthread(L, -1)) { /* ... */ }
```


----


### <span class="subsection">`lua_isnone`</span>

<span class="signature">`int lua_isnone(lua_State* L, int idx)`</span>
<span class="stack">`[-0, +0, -]`</span>

- `L`: Lua thread
- `idx`: Stack index


Checks if the value at the given stack index is none.

```cpp title="Example"
if (lua_isnone(L, -1)) { /* ... */ }
```


----


### <span class="subsection">`lua_isnoneornil`</span>

<span class="signature">`int lua_isnoneornil(lua_State* L, int idx)`</span>
<span class="stack">`[-0, +0, -]`</span>

- `L`: Lua thread
- `idx`: Stack index


Checks if the value at the given stack index is none or nil.

```cpp title="Example"
if (lua_isnoneornil(L, -1)) { /* ... */ }
```


----


### <span class="subsection">`luaL_typename`</span>

<span class="signature">`const char* luaL_typename(lua_State* L, int idx)`</span>
<span class="stack">`[-0, +0, -]`</span>

- `L`: Lua thread
- `idx`: Stack index


Returns the name of the type at the given index.

```cpp title="Example"
lua_pushvector(L, 10, 20, 30);
const char* t_name = luaL_typename(L, -1);
printf("Type: %s\n", t_name); // "Type: vector"
```


----


## String Buffer Functions

### <span class="subsection">`luaL_buffinit`</span>

<span class="signature">`void luaL_buffinit(lua_State* L, luaL_Buffer* B)`</span>
<span class="stack">`[-0, +0, -]`</span>

- `L`: Lua thread
- `B`: Lua string buffer


Initializes a string buffer.

```cpp title="Example"
luaL_Strbuf b;
luaL_buffinit(L, &b);
```


----


### <span class="subsection">`luaL_buffinitsize`</span>

<span class="signature">`char* luaL_buffinitsize(lua_State* L, luaL_Buffer* B, size_t size)`</span>
<span class="stack">`[-0, +0, -]`</span>

- `L`: Lua thread
- `B`: Lua string buffer
- `size`: Preallocated size


Initializes a string buffer with an initial allocated size. A pointer to the start of the buffer is returned.

```cpp title="Example"
luaL_Strbuf b;
char* buf = luaL_buffinitsize(L, &b, 512);
```


----


### <span class="subsection">`luaL_prepbuffsize`</span>

<span class="signature">`char* luaL_prepbuffsize(luaL_Buffer* B, size_t size)`</span>
<span class="stack">`[-0, +0, -]`</span>

- `B`: Lua string buffer
- `size`: Size extension


Ensure the string buffer has at least `size` capacity available. For instance, if 10 characters need to be added to an existing string buffer, it may be more optimal to call `luaL_prepbuffsize(&b, 10)` before adding each character.


----


### <span class="subsection">`luaL_addchar`</span>

<span class="signature">`void luaL_addchar(luaL_Buffer* B, char c)`</span>
<span class="stack">`[-0, +0, -]`</span>

- `B`: Lua string buffer
- `c`: Character


Adds a character to a string buffer.


----


### <span class="subsection">`luaL_addlstring`</span>

<span class="signature">`void luaL_addlstring(luaL_Buffer* B, const char* s, size_t l)`</span>
<span class="stack">`[-0, +0, -]`</span>

- `B`: Lua string buffer
- `s`: String
- `l`: String length


Adds a string to a string buffer.


----


### <span class="subsection">`luaL_addstring`</span>

<span class="signature">`void luaL_addstring(luaL_Buffer* B, const char* s)`</span>
<span class="stack">`[-0, +0, -]`</span>

- `B`: Lua string buffer
- `s`: String


Adds a string to a string buffer. If the length of the string is known, use `luaL_addlstring` instead.


----


### <span class="subsection">`luaL_addvalue`</span>

<span class="signature">`void luaL_addvalue(luaL_Buffer* B)`</span>
<span class="stack">`[-1, +0, -]`</span>

- `B`: Lua string buffer


Pops a value from the top of the stack and adds it to the buffer.


----


### <span class="subsection">`luaL_addvalueany`</span>

<span class="signature">`void luaL_addvalueany(luaL_Buffer* B, int idx)`</span>
<span class="stack">`[-0, +0, -]`</span>

- `B`: Lua string buffer
- `idx`: Stack index


Adds the value at the given stack index into the buffer. Unlike `luaL_addvalue`, this does _not_ pop the item from the stack.


----


### <span class="subsection">`luaL_pushresult`</span>

<span class="signature">`void luaL_pushresult(luaL_Buffer* B)`</span>
<span class="stack">`[-0, +1, -]`</span>

- `B`: Lua string buffer


Pushes the result of the string buffer onto the stack.


----


### <span class="subsection">`luaL_pushresultsize`</span>

<span class="signature">`void luaL_pushresultsize(luaL_Buffer* B, size_t size)`</span>
<span class="stack">`[-0, +1, -]`</span>

- `B`: Lua string buffer
- `size`: Size


Pushes the result of the string buffer onto the stack, assuming `size` extra length on the buffer. This is only used if the buffer is being directly written rather than going through other string buffer functions that track the size.

```cpp title="Example" hl_lines="9"
// Copied from luau/VM/src/lstrlib.cpp

// Note how the buffer is initialized to the correct size, but
// the buffer is being written to directly, rather than going
// through the `luaL_addchar` function.
static int str_lower(lua_State* L) {
	size_t l;
	const char* s = luaL_checklstring(L, 1, &l);
	luaL_Strbuf b;
	char* ptr = luaL_buffinitsize(L, &b, l); // buffer initialized
	for (size_t i = 0; i < l; i++) {
		*ptr++ = tolower(uchar(s[i])); // direct write
	}
	luaL_pushresultsize(&b, l); // push result
	return 1;
}
```


----


## Debug Functions

### <span class="subsection">`lua_stackdepth`</span>

<span class="signature">`int lua_stackdepth(lua_State* L)`</span>
<span class="stack">`[-0, +0, -]`</span>

- `L`: Lua thread


Returns the current stack depth.


----


### <span class="subsection">`lua_getinfo`</span>

<span class="signature">`int lua_getinfo(lua_State* L, int level, const char* what, lua_Debug* ar)`</span>
<span class="stack">`[-0, +(0|1), -]`</span>

- `L`: Lua thread
- `level`: Stack level
- `what`: Desired information
- `ar`: Debug info (activation record)


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


----


### <span class="subsection">`lua_getargument`</span>

<span class="signature">`int lua_getargument(lua_State* L, int level, int n)`</span>
<span class="stack">`[-0, +(0|1), -]`</span>

- `L`: Lua thread
- `level`: Stack level
- `n`: Argument number


Gets argument `n` at the given stack level. If found, the value is pushed to the top of the stack and the function returns `1`. Otherwise, the function returns `0` and nothing is pushed to the stack.


----


### <span class="subsection">`lua_getlocal`</span>

<span class="signature">`int lua_getlocal(lua_State* L, int level, int n)`</span>
<span class="stack">`[-0, +(0|1), -]`</span>

- `L`: Lua thread
- `level`: Stack level
- `n`: Argument number


Gets a local variable at the given stack level and pushes the value onto the stack. The name of the local variable is returned, and the value on the stack is popped. If no local is found, `NULL` is returned and nothing is pushed to the stack.


----


### <span class="subsection">`lua_setlocal`</span>

<span class="signature">`int lua_setlocal(lua_State* L, int level, int n)`</span>
<span class="stack">`[-(0|1), +0, -]`</span>

- `L`: Lua thread
- `level`: Stack level
- `n`: Argument number


Sets a local variable at the given stack level to the value at the top of the stack. The name of the local variable is returned, and the value on the stack is popped. If no local is found, `NULL` is returned and nothing is popped from the stack.


----


### <span class="subsection">`lua_getupvalue`</span>

<span class="signature">`int lua_getupvalue(lua_State* L, int level, int n)`</span>
<span class="stack">`[-0, +(0|1), -]`</span>

- `L`: Lua thread
- `level`: Stack level
- `n`: Argument number


Pushes an upvalue to the stack, and returns its name. If not found, returns `NULL` and nothing is pushed to the stack.


----


### <span class="subsection">`lua_setupvalue`</span>

<span class="signature">`int lua_setupvalue(lua_State* L, int level, int n)`</span>
<span class="stack">`[-0, +(0|1), -]`</span>

- `L`: Lua thread
- `level`: Stack level
- `n`: Argument number


Pops a value off the stack and sets the given upvalue with the popped value, and returns its name. If not found, returns `NULL` and nothing is popped from the stack.


----


### <span class="subsection">`lua_singlestep`</span>

<span class="signature">`int lua_singlestep(lua_State* L, int enabled)`</span>
<span class="stack">`[-0, +0, -]`</span>

- `L`: Lua thread
- `enabled`: Enabled


Enables or disables single-step mode.


----


### <span class="subsection">`lua_breakpoint`</span>

<span class="signature">`int lua_breakpoint(lua_State* L, int funcindex, int line, int enabled)`</span>
<span class="stack">`[-0, +0, -]`</span>

- `L`: Lua thread
- `funcindex`: Function index
- `line`: Line
- `enabled`: Enabled


Enables or disables a breakpoint at the given line within the given function at `funcindex` on the stack.


----


### <span class="subsection">`lua_getcoverage`</span>

<span class="signature">`void lua_getcoverage(lua_State* L, int funcindex, void* context, lua_Coverage callback)`</span>
<span class="stack">`[-0, +0, -]`</span>

- `L`: Lua thread
- `funcindex`: Function index
- `context`: Context
- `callback`: Coverage callback function


Get coverage.


----


### <span class="subsection">`lua_debugtrace`</span>

<span class="signature">`const char* lua_debugtrace(lua_State* L)`</span>
<span class="stack">`[-0, +0, -]`</span>

- `L`: Lua thread


Gets a traceback string.

**Note:** Internally, this uses a static string buffer. Thus, this function is not thread-safe, nor is it safe to hold onto the returned value. Create a copy of the returned string if needed.


----


### <span class="subsection">`luaL_where`</span>

<span class="signature">`void luaL_where(lua_State* L, int level)`</span>
<span class="stack">`[-0, +1, -]`</span>

- `L`: Lua thread
- `level`: Stack level


Pushes a string onto the stack containing the short source and current line, e.g. `"some/script.luau:10: "`. This is often used as a prefix for other debug logging information.
