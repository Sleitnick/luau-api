---
name: lua_callmeta
ret: int
stack: "-0, +(0|1), -"
args:
  - name: L
    type: lua_State*
    desc: Lua thread
  - name: idx
    type: int
    desc: Stack index
  - name: field
    type: const char*
    desc: Metatable field
---

Attempts to call the given metatable function for the table at `idx`. If the table doesn't have a metatable, or the metatable doesn't have `field`, then this function returns `0` and nothing is pushed onto the stack. Otherwise, the function returns `1` and the result of the called metatable function is pushed onto the stack.

```cpp title="Example"
// Assume the top of the stack is a table

if (lua_callmeta(L, -1, "__tostring")) {
	const char* result = lua_tostring(L, -1);
	lua_pop(L, 1);
	// ...
}
```
