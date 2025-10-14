---
name: lua_newbuffer
ret: void*
stack: "-0, +1, -"
args:
  - name: L
    type: lua_State*
    desc: Lua thread
  - name: sz
    type: size_t
    desc: Size
---

Pushes a new buffer to the stack and returns a pointer to the buffer. Buffers are just arbitrary data. Luau can create and interact with buffers through the [`buffer` library](https://luau.org/library#buffer-library). Use the [`lua_tobuffer`](#lua_tobuffer) function to retrieve a buffer from the stack.

```cpp title="Example" hl_lines="8"
struct Foo {
	int n;
}

// As an example, write 'Foo' to a buffer:
Foo foo{};
foo.n = 10;
void* buf = lua_newbuffer(L, sizeof(Foo));
memcpy(buf, &foo, sizeof(Foo));
```
