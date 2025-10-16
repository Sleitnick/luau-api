---
name: lua_setuserdatadtor
ret: int
stack: "-0, +0, -"
args:
  - name: L
    type: lua_State*
    desc: Lua thread
  - name: tag
    type: int
    desc: Tag
  - name: dtor
    type: lua_Destructor
    desc: Tag
---

Assigns the destructor function for a given userdata tag. All userdata with the given tag will utilize this destructor during GC.

```cpp title="Example" hl_lines="17"
constexpr int kFooTag = 10;

struct Foo {
	char* some_allocated_data;
};

static void Foo_destructor(lua_State* L, void* data) {
	Foo* foo = static_cast<Foo*>(data);
	delete foo->some_allocated_data;
}

void setup_Foo(lua_State* L) {
	luaL_newmetatable(L, "Foo");
	// ...build metatable
	lua_setuserdatametatable(L, kFooTag);

	lua_setuserdatadtor(L, kFooTag, Foo_destructor);
}
```
