# Light Userdata

A light userdata value simply wraps a pointer to data that you manage. This is useful when you want to share a non-Luau-managed value somewhere within Luau, e.g. the Luau registry.

Luau does not assume ownership of the memory pointed to by the light userdata. You are responsible for the memory.

## Example

```cpp
struct Foo {};

// Memory of foo owned by our program; not owned by Luau
Foo* foo = new Foo();

// Store a pointer to foo within the registry:
lua_pushlightuserdata(L, foo);
lua_rawsetfield(L, LUA_REGISTRYINDEX, "Foo");

// Retrieve foo:
lua_rawgetfield(L, LUA_REGISTRYINDEX, "Foo");
Foo* foo = static_cast<Foo*>(lua_tolightuserdata(L, -1));
lua_pop(L, 1); // pop the lightuserdata value

// We are responsible for freeing foo:
delete foo;
```

## Tags

Similar to userdata types, light userdata can also be assigned a tag. This can help ensure we don't type-cast to the wrong type. If we call `lua_tolightuserdatatagged` on a light userdata with the incorrect tag, it will simply return `NULL`.

```cpp
constexpr int kFooTag = 10;

Foo* foo = new Foo();

// Push with tag:
lua_pushlightuserdatatagged(L, foo, kFooTag);

// Retrieve with tag:
Foo* f = static_cast<Foo*>(lua_tolightuserdatatagged(L, -1, kFooTag));
```
