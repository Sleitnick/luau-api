---
name: lua_newstate
ret: lua_State*
stack: "-0, +0, -"
args:
  - name: f
    type: lua_Alloc
    desc: Luau allocator function. All allocations made by Luau (including the construction of the state) are done through this allocator.
  - name: ud
    type: void*
    desc: Opaque userdata pointer that is passed to the allocator function.
---

Creates a new Luau state. If the allocator fails to allocate
memory for the new state, this function will return `nullptr`.
Use `lua_close()` to close the state once done.

??? note "Example"
	``` cpp hl_lines="1"
	lua_State* L = lua_newstate(allocator, nullptr);
	lua_close(L);
	```

??? note "Allocator Example"
	``` cpp
	static void* allocator(void* ud, void* ptr, size_t old_size, size_t new_size) {
	(void)ud; (void)old_size; // Not using these

	// new_size of 0 indicates the allocator should free the ptr
	if (new_size == 0) {
		free(ptr);
		return nullptr;
	}

	return realloc(ptr, new_size);
	}

	lua_State* L = lua_newstate(allocator, nullptr);
	```
