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


----


## Access Functions

### <span class="subsection">`lua_isnumber`</span>

<span class="signature">`int lua_isnumber(lua_State* L, int idx)`</span>
<span class="stack">`[-0, +0, -]`</span>

- `L`: Lua thread
- `idx`: Stack index


Returns `1` if the value at stack index `idx` is a number _or_ the value is a string that can be coerced to a number. Otherwise, returns `0`.


----


### <span class="subsection">`lua_isstring`</span>

<span class="signature">`int lua_isstring(lua_State* L, int idx)`</span>
<span class="stack">`[-0, +0, -]`</span>

- `L`: Lua thread
- `idx`: Stack index


Returns `1` if the value at the given stack index is a string _or_ a number (all numbers can be converted to a string). Otherwise, returns `0`.


----


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


### <span class="subsection">`lua_isuserdata`</span>

<span class="signature">`int lua_isuserdata(lua_State* L, int idx)`</span>
<span class="stack">`[-0, +0, -]`</span>

- `L`: Lua thread
- `idx`: Stack index


Returns `1` if the value at the given stack index is a userdata object. Otherwise, returns `0`.


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


### <span class="subsection">`lua_tounsignedx`</span>

<span class="signature">`int lua_tounsignedx(lua_State* L, int idx, int* isnum)`</span>
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


### <span class="subsection">`lua_tostringatom`</span>

<span class="signature">`const char* lua_tostringatom(lua_State* L, int idx, int* atom)`</span>
<span class="stack">`[-0, +0, m]`</span>

- `L`: Lua thread
- `idx`: Stack index
- `atom`: Atom


Identical to [`lua_tostring`](#lua_tostring), except the string atom is written to the `atom` argument. See the [Atoms](cookbook/atoms.md) page for more information on string atoms.


----


### <span class="subsection">`lua_tolstringatom`</span>

<span class="signature">`const char* lua_tolstringatom(lua_State* L, int idx, size_t len, int* atom)`</span>
<span class="stack">`[-0, +0, m]`</span>

- `L`: Lua thread
- `idx`: Stack index
- `len`: String length
- `atom`: Atom


Identical to [`lua_tolstring`](#lua_tolstring), except the string atom is written to the `atom` argument. See the [Atoms](cookbook/atoms.md) page for more information on string atoms.


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


Returns a pointer to a lightuserdata on the stack. Returns `NULL` if the value is not a lightuserdata _or_ if the attached tag does not equal the provided `tag` argument. For more info on tags, see the [Tags](cookbook/tags.md) page.

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


### <span class="subsection">`lua_touserdata`</span>

<span class="signature">`void* lua_touserdata(lua_State* L, int idx)`</span>
<span class="stack">`[-0, +0, -]`</span>

- `L`: Lua thread
- `idx`: Stack index


Returns a pointer to a userdata on the stack. Returns `NULL` if the value is not a userdata.

If it is preferred to throw an error if the value is not a userdata, use the `luaL_checkuserdata` function instead.

**Note:** It may be unsafe to hang onto a pointer to a userdata value. The Luau GC owns the userdata memory, and may free it. See the page on [pinning](cookbook/pinning.md) for tips on keeping a value from being GC'd, or consider using [light userdata](cookbook/light-userdata.md) instead.

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


Returns a pointer to a tagged userdata on the stack. Returns `NULL` if the value is not a userdata _or_ the userdata's tag does not match the provided `tag` argument. For more info on tags, see the [Tags](cookbook/tags.md) page.

**Note:** It may be unsafe to hang onto a pointer to a userdata value. The Luau GC owns the userdata memory, and may free it. See the page on [pinning](cookbook/pinning.md) for tips on keeping a value from being GC'd, or consider using [light userdata](cookbook/light-userdata.md) instead.

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
const char* s = lua_pushfstringL(L, "number: %d", 32);
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


### <span class="subsection">`lua_pushlightuserdatatagged`</span>

<span class="signature">`void lua_pushlightuserdatatagged(lua_State* L, void* p, int tag)`</span>
<span class="stack">`[-0, +1, -]`</span>

- `L`: Lua thread
- `p`: Pointer to arbitrary user-owned data
- `tag`: Tag


Pushes the tagged lightuserdata to the stack. Use [`lua_tolightuserdatatagged`](#lua_tolightuserdatatagged) to retrieve the value. For more info on tags, see the [Tags](cookbook/tags.md) page.

```cpp title="Example" hl_lines="6"
constexpr int kFooTag = 1;
struct Foo {};

Foo* foo = new Foo();

lua_pushlightuserdatatagged(L, foo, kFooTag);
```


----


### <span class="subsection">`lua_newuserdatatagged`</span>

<span class="signature">`void* lua_newuserdatatagged(lua_State* L, size_t sz, int tag)`</span>
<span class="stack">`[-0, +1, -]`</span>

- `L`: Lua thread
- `sz`: Size of the data
- `tag`: Tag


Creates the tagged userdata and pushes it to the stack. A pointer to the newly-constructed data is returned. Use [`lua_touserdatatagged`](lua_touserdatatagged) to retrieve the value. For more info on tags, see the [Tags](cookbook/tags.md) page.

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


Creates the tagged userdata with a pre-defined metatable and pushes it to the stack. A pointer to the newly-constructed data is returned. Use [`lua_touserdatatagged`](lua_touserdatatagged) to retrieve the value. For more info on tags, see the [Tags](cookbook/tags.md) page.

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


### <span class="subsection">`lua_newuserdatadtor`</span>

<span class="signature">`void* lua_newuserdatadtor(lua_State* L, size_t sz, void (*dtor)(void*))`</span>
<span class="stack">`[-0, +1, -]`</span>

- `L`: Lua thread
- `sz`: Size of the data
- `dtor`: Destructor


Creates a new userdata with an assigned destructor. Destructors are called when Luau is freeing up the userdata memory.

To assign a destructor for all userdata of a given tag, use [`lua_setuserdatadtor`](#lua_setuserdatadtor).

```cpp title="Example" hl_lines="5-8"
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
