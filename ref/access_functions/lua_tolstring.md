---
name: lua_tolstring
ret: const char*
stack: "-0, +0, m"
args:
  - name: L
    type: lua_State*
    desc: Lua thread
  - name: idx
    type: int
    desc: Stack index
  - name: len
    type: size_t
    desc: String length
---

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
