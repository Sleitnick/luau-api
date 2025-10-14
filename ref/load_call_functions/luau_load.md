---
name: luau_load
ret: int
stack: "-0, +1, -"
args:
  - name: L
    type: lua_State*
    desc: Lua thread
  - name: chunkname
    type: const char*
    desc: Chunk name
  - name: data
    type: const char*
    desc: Bytecode data
  - name: size
    type: size_t
    desc: Bytecode data size
  - name: env
    type: int
    desc: Environment
---

Loads bytecode onto the given thread as a callable function on the top of the stack. If loading fails, the error message is pushed to the stack instead.

The `chunkname` argument helps with debugging.

Set `env` to `0` to use the default environment. Otherwise, this indicates the stack index for the given environment to use.

```cpp title="Example" hl_lines="6"
const char* source = "print('hello')";

size_t bytecode_size;
char* bytecode = luau_compile(source, strlen(source), nullptr, &bytecode_size);

int res = luau_load(L, "=test", bytecode, bytecode_size, 0);
free(bytecode);

if (res != 0) {
	size_t len;
	const char* msg = lua_tolstring(L, -1, &len);
	lua_pop(L, 1);
	printf("failed to compile: %s\n", msg);
	return;
}

// Move loaded chunk to its own thread and run it:
lua_State* T = lua_newthread(L);
lua_pushvalue(L, -2);
lua_remove(L, -3);
lua_xmove(L, T, 1);
int status = lua_resume(T, nullptr, 0);
// ...handle status
```
