# Buffers

In Luau, buffers are arbitrary chunks of memory. Luau can interact with these values through the [`buffer`](https://luau.org/library#buffer-library) library.

Buffers are useful when Luau needs to interact with raw data. Buffers cannot be resized, but they can be modified.

```cpp
// Allow Luau to fetch the binary contents of a file:
int read_file(lua_State* L) {
    const char* filepath = luaL_checkstring(L, 1);
    std::ifstream file(filepath, std::ios::binary);
    if (!file.is_open()) {
        luaL_error("failed to open file: %s", filepath);
    }

    std::string data;
    std::string line;
    while (std::getline(file, line)) {
        data += line;
    }

    // Create Luau buffer:
    void* buf = lua_newbuffer(L, data.size());

    // Write to buffer:
    memcpy(buf, data.data(), data.size());

    return 1;
}

// Expose to Luau:
lua_pushcfunction(L, read_file, "read_file");
lua_setglobal(L, "read_file");
```

Now we can read a file from Luau:
```luau
local filepath = "some/path/whatever.jpg"
local buf = read_file(filepath)
print(`size of {filepath}: {buffer.len(buf)}`)
```
