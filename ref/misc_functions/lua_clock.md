---
name: lua_clock
ret: double
stack: "-0, +0, -"
args:
---

Returns high-precision timestamp in seconds from the OS. This is exactly what the Luau library function `os.clock` uses. Here is the OS Clock function implementation:

```cpp title="example" hl_lines="3"
// Copied from luau/VM/src/loslib.cpp
static int os_clock(lua_State* L) {
	lua_pushnumber(L, lua_clock());
	return 1;
}
```
