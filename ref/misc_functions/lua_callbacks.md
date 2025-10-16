---
name: lua_callbacks
ret: lua_Callbacks*
stack: "-0, +0, -"
args:
  - name: L
    type: lua_State*
    desc: Lua thread
---

Allows users to install callback functions for various purposes.

```cpp title="Example"
// Handle Luau panics (only when Luau is built with longjmp, not C++ exceptions)
static void handle_panic(lua_State* L, int errcode) {
	fprintf(stderr, "luau panic: %d\n", errcode);
}

// Called when thread 'L' is created or destroyed, denoted if LP (L parent) exists or is null
static void handle_user_thread(lua_State* LP, lua_State* L) {
	if (LP == nullptr) {
		// L was destroyed
	} else {
		// L was created
	}
}

lua_callbacks(L)->panic = handle_panic;
lua_callbacks(L)->userthread = handle_user_thread;
// ...
```
