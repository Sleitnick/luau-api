---
name: luaL_optlstring
ret: const char*
stack: "-0, +0, -"
args:
  - name: L
    type: lua_State*
    desc: Lua thread
  - name: idx
    type: int
    desc: Stack index
  - name: def
    type: const char*
    desc: Default string
  - name: len
    type: size_t
    desc: String length
---

Gets the string at the given stack index. If the value at the given index is nil or none, then `def` is returned instead. Otherwise, an error is thrown.

```cpp title="Example"
int send_message(lua_State* L) {
	size_t message_len;
	const char* message = luaL_optlstring(L, 1, "Default message", &message_len);
}
```
