# Luau C API Reference

## State Manipulation

### <span class="subsection">`lua_newstate`</span>

<span class="signature">`lua_State* lua_newstate(lua_Alloc f, void* ud)`</span>
<span class="stack">`[-0, +0, -]`</span>

- `f`: Luau allocator function. All allocations made by Luau (including the construction of the state) are done through this allocator.
- `ud`: Opaque userdata pointer that is passed to the allocator function.

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


### <span class="subsection">`lua_close`</span>

<span class="signature">`void lua_close()`</span>
<span class="stack">`[-0, +0, -]`</span>

Closes the Luau state. Luau objects are garbage collected and any dynamic memory is freed.

??? note "Example"
    ``` cpp
    lua_close(L);
    ```

??? note "Smart Pointer"
    ``` cpp
    // TODO: Show smart pointer example wrapping around the state.
    ```
