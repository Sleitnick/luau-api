---
name: lua_setglobal
ret: void
stack: "-1, +0, -"
args:
  - name: L
    type: lua_State*
    desc: Lua thread
  - name: k
    type: const char*
    desc: Field
---

Places the value at the top of the stack into the global table at key `k`. The value is popped from the stack. Use [`lua_getglobal`](#lua_getglobal) to retrieve the value.

As implied by the name, globals are globally-accessible to Luau.

```cpp title="Example"
lua_pushliteral(L, "hello");
lua_setglobal(L, "message"); // _G.message = "hello"
```

```luau title="Luau Example"
print(message) -- "hello"
```
