---
name: lua_next
ret: int
stack: "-1, +(2|0), -"
args:
  - name: L
    type: lua_State*
    desc: Lua thread
  - name: idx
    type: int
    desc: Stack index
---

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
