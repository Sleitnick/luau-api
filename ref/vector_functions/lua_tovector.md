---
name: lua_tovector
ret: const float*
stack: "-0, +0, -"
args:
  - name: L
    type: lua_State*
    desc: Lua thread
  - name: idx
    type: int
    desc: Stack index
---

Returns the vector at the given Luau index, or `NULL` if not a vector.

By default, vectors in Luau are 3-wide. Luau can be built with the `LUA_VECTOR_SIZE` preprocessor set to `4` for 4-wide vectors.

```cpp title="Example" hl_lines="3"
lua_pushvector(L, 3, 5, 2); // x, y, z

const float* vec = lua_tovector(L, -1);

float x = vec[0];
float y = vec[1];
float z = vec[2];
printf("%f, %f, %f\n", x, y, z);
```
