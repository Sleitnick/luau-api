# Luau C API Reference

### <span class="section">`State Manipulation`</span>

<span class="signature">`lua_State* lua_newstate lua_Alloc f, void* ud`</span>
<span class="stack">`[-0, +0, -]`</span>

- f: Luau allocator function.
- ud: Opaque userdata pointer that is passed to the allocator function.

Hello world! This is the newstate description.
