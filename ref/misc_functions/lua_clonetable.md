---
name: lua_clonetable
ret: void
stack: "-0, +1, -"
args:
  - name: L
    type: lua_State*
    desc: Lua thread
  - name: idx
    type: int
    desc: Stack index
---

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
