---
name: lua_setmemcat
ret: int
stack: "-0, +0, -"
args:
  - name: L
    type: lua_State*
    desc: Lua thread
  - name: category
    type: int
    desc: Memory category
---

Set the memory category for a given thread (the default is `0`). There is no associated function to retrieve a thread's current memory category.

Call [`lua_totalbytes`](#lua_totalbytes) to query the amount of memory utilized by a given memory category.

**Note:** While the `category` parameter is an `int`, the actual memory category attached to the thread is a `uint8_t`, and thus the category parameter is cast to `uint8_t`. Therefore, memory categories are limited to the range `[0, 255]`.

```cpp title="Example"
// Set the memory category of `L` to 10:
lua_setmemcat(L, 10);
```
