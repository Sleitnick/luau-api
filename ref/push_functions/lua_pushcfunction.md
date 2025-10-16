---
name: lua_pushcfunction
ret: void
stack: "-0, +1, -"
args:
  - name: L
    type: lua_State*
    desc: Lua thread
  - name: fn
    type: lua_CFunction
    desc: C Function
  - name: debugname
    type: const char*
    desc: Debug name
---

Pushes the C function to the stack.

Equivalent to `lua_pushcclosurek`, but without any upvalues nor any continuation function.

```cpp title="Example" hl_lines="6"
int multiply(lua_State* L) {
	lua_pushnumber(L, lua_tonumber(L, 1) * lua_tonumber(L, 2));
	return 1;
}

lua_pushcfunction(L, multiply, "multiply");
lua_setglobal(L, "multiply");
```

```luau title="Luau Example"
print("2 * 5 = " .. multiply(2, 5))
```
