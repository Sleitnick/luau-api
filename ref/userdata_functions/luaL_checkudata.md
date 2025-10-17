---
name: luaL_checkudata
ret: void*
stack: "0, +0, -"
args:
  - name: L
    type: lua_State*
    desc: Lua thread
  - name: ud
    type: int
    desc: Userdata index
  - name: name
    type: const char*
    desc: Name
---

Asserts that a value on the stack is a userdata with a matching metatable to `name` (created with [`luaL_newmetatable`](#lual_newmetatable)).

```cpp title="Example" hl_lines="6"
constexpr const char* kFoo = "Foo";

struct Foo { /* ... */ };

Foo* check_Foo(lua_State* L, int idx) {
	return static_cast<Foo*>(luaL_checkudata(L, kFoo));
}
```
