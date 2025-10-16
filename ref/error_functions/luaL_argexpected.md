---
name: luaL_argexpected
ret: l_noret
stack: "-0, +0, -"
args:
  - name: L
    type: lua_State*
    desc: Lua thread
  - name: cond
    type: int
    desc: Condition
  - name: narg
    type: int
    desc: Argument number
  - name: tname
    type: const char*
    desc: Type name
---

Throws a Luau error with a templated error message for an incorrect type. This is similar to `luaL_typeerror`, except it encapsulates a condition, similar to an assertion.

```cpp title="Example"
int send_table(lua_State* L) {
	// expects a table as the first argument
	luaL_argexpected(L, lua_istable(L, 1), 1, "table");

	// ...
}
```
