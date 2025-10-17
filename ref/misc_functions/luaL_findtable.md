---
name: luaL_findtable
ret: const char*
stack: "-0, +1, -"
args:
  - name: L
    type: lua_State*
    desc: Lua thread
  - name: idx
    type: int
    desc: Stack index
  - name: fname
    type: const char*
    desc: Name
  - name: szhint
    type: int
    desc: Size hint
---

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
