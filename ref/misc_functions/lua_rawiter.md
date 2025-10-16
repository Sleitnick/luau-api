---
name: lua_rawiter
ret: int
stack: "-0, +2, -"
args:
  - name: L
    type: lua_State*
    desc: Lua thread
  - name: idx
    type: int
    desc: Stack index
  - name: iter
    type: int
    desc: Iterator
---

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
