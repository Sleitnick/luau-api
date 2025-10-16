---
name: lua_pushvector
ret: void
stack: "-0, +1, -"
args:
  - name: L
    type: lua_State*
    desc: Lua thread
  - name: x
    type: float
    desc: X
  - name: y
    type: float
    desc: Y
  - name: z
    type: float
    desc: Z
---

Pushes a vector to the Luau stack. Luau comes with a [vector library](https://luau.org/library#vector-library) for operating against vector values.

**Note:** Unlike Luau numbers being double-precision floating point numbers, Luau vector values are single-precision floats.

```cpp title="Example 3-wide" hl_lines="1"
// By default, Luau vectors are 3-wide

lua_pushvector(L, 10, 15, 20);

const char* v = lua_tovector(L, -1);
float x = v[0]; // 10
float y = v[1]; // 15
float z = v[2]; // 20
```

If Luau is built with the `LUA_VECTOR_SIZE` preprocessor set to `4`, then this will be a 4-wide vector, and the function will have an additional `w` parameter.
```cpp title="Example 4-wide" hl_lines="1"
// If Luau is built with LUA_VECTOR_SIZE=4

lua_pushvector(L, 10, 15, 20, 25);

const char* v = lua_tovector(L, -1);
float x = v[0]; // 10
float y = v[1]; // 15
float z = v[2]; // 20
float w = v[3]; // 25
```
