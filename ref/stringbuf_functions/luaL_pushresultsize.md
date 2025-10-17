---
name: luaL_pushresultsize
ret: void
stack: "-0, +1, -"
args:
  - name: B
    type: luaL_Buffer*
    desc: Lua string buffer
  - name: size
    type: size_t
    desc: Size
---

Pushes the result of the string buffer onto the stack, assuming `size` extra length on the buffer. This is only used if the buffer is being directly written rather than going through other string buffer functions that track the size.

```cpp title="Example" hl_lines="9"
// Copied from luau/VM/src/lstrlib.cpp

// Note how the buffer is initialized to the correct size, but
// the buffer is being written to directly, rather than going
// through the `luaL_addchar` function.
static int str_lower(lua_State* L) {
	size_t l;
	const char* s = luaL_checklstring(L, 1, &l);
	luaL_Strbuf b;
	char* ptr = luaL_buffinitsize(L, &b, l); // buffer initialized
	for (size_t i = 0; i < l; i++) {
		*ptr++ = tolower(uchar(s[i])); // direct write
	}
	luaL_pushresultsize(&b, l); // push result
	return 1;
}
```
