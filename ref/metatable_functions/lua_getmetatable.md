---
name: lua_getmetatable
ret: int
stack: "-0, +(0|1), -"
args:
  - name: L
    type: lua_State*
    desc: Lua thread
  - name: idx
    type: int
    desc: Stack index
---

Gets the metatable for the object at the given stack index. If the metatable is found, it is pushed to the top of the stack and the function returns `1`. Otherwise, the function returns `0` and the stack remains the same.

```cpp title="Example"
if (lua_getmetatable(L, -1)) {
	// Metatable is now at the top of the stack
}
```
