---
name: lua_tocfunction
ret: lua_CFunction
stack: "-0, +0, -"
args:
  - name: L
    type: lua_State*
    desc: Lua thread
  - name: idx
    type: int
    desc: Stack index
---

Returns the C function at the given stack position. If the value is not a C function, this function returns `NULL`.

```cpp title="Example" hl_lines="6"
int hello() {
  printf("hello\n");
  return 0;
}

lua_pushcfunction(L, hello, "hello");

lua_CFunction f = lua_tocfunction(L, -1);
if (f) {
  f(); // hello
}
```
