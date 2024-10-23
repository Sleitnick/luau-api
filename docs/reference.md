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

``` cpp title="Example" hl_lines="1"
lua_State* L = lua_newstate(allocator, nullptr);
lua_close(L);
```
