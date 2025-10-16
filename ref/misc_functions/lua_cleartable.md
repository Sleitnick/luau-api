---
name: lua_cleartable
ret: void
stack: "-0, +0, -"
args:
  - name: L
    type: lua_State*
    desc: Lua thread
  - name: idx
    type: int
    desc: Stack index
---

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
