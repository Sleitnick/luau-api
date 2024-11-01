---
name: lua_checkstack
ret: int
stack: "-0, +0, m"
args:
  - name: L
    type: lua_State*
    desc: Lua thread
  - name: size
    type: int
    desc: Desired stack size
---

Ensures the stack is large enough to hold `size` _more_ elements. This will only grow the stack, not shrink it. Returns true if successful, or false if it fails (e.g. the max stack size exceeded).

```cpp title="Example" hl_lines="2"
// Ensure there are at least 2 more slots on the stack:
if (lua_checkstack(L, 2)) {
	lua_pushinteger(L, 10);
	lua_pushinteger(L, 20);
}
```
