---
name: lua_getuserdatadtor
ret: lua_Destructor
stack: "-0, +0, -"
args:
  - name: L
    type: lua_State*
    desc: Lua thread
  - name: tag
    type: int
    desc: Tag
---

Returns the destructor function assigned to the userdata tag.

```cpp title="Example" hl_lines="7 11"
constexpr int kFooTag = 10;
struct Foo {};
static void Foo_destructor(lua_State* L, void* data) {}

void setup_Foo(lua_State* L) {
	// ...
	auto dtor_before = lua_getuserdatadtor(L, kFooTag); // dtor_before == nullptr

	lua_setuserdatadtor(L, kFooTag, Foo_destructor);

	auto dtor_after = lua_getuserdatadtor(L, kFooTag); // dtor_after == Foo_destructor
}
```
