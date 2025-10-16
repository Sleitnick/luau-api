---
name: luaL_checklstring
ret: const char*
stack: "-0, +0, -"
args:
  - name: L
    type: lua_State*
    desc: Lua thread
  - name: idx
    type: int
    desc: Stack index
  - name: len
    type: size_t
    desc: String length
---

Similar to [`lua_tolstring`](#lua_tolstring), except the type will be asserted. If the value is not a string, an error will be thrown.

```cpp title="Example"
int send_message(lua_State* L) {
	size_t message_len;
	const char* message = luaL_checklstring(L, 1, &message_len);
}
```
