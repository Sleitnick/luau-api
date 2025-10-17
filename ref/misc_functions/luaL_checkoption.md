---
name: luaL_checkoption
ret: int
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
    desc: Default option
  - name: lst[]
    type: const char* const
    desc: Options list
---

Asserts the value at the given index is a string within the given options list `lst`. If `def` is provided (non-null), then `def` will be used as the default option if the value at the given stack index is nil or none. If the assertion passes, the index to the item in the list is returned.

```cpp title="Example"
int set_mode(lua_State* L) {
	static const char* const options[] = {"follow", "defend", "attack", "flee", nullptr};

	int i = luaL_checkoption(L, 1, options[0], options);
	const char* option = options[i];
	// ...
}
```
