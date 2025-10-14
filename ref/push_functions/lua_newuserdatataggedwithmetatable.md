---
name: lua_newuserdatataggedwithmetatable
ret: void*
stack: "-0, +1, -"
args:
  - name: L
    type: lua_State*
    desc: Lua thread
  - name: sz
    type: size_t
    desc: Size of the data
  - name: tag
    type: int
    desc: Tag
---

Creates the tagged userdata with a pre-defined metatable and pushes it to the stack. A pointer to the newly-constructed data is returned. Use [`lua_touserdatatagged`](lua_touserdatatagged) to retrieve the value. For more info on tags, see the [Tags](cookbook/tags.md) page.

Using this method is faster than attempting to assign a metatable to new userdata every construction, e.g. using `luaL_newmetatable`. Instead, the metatable is created ahead of time using `lua_setuserdatametatable`, linked to the userdata's tag.

```cpp title="Example" hl_lines="35"
constexpr int kFooTag = 1;

struct Foo {
	int n;
};

int Foo_index(lua_State* L) {
	Foo* foo = static_cast<Foo*>(luaL_touserdatatagged(L, 1, kFooTag));
	const char* property = lua_tostring(L, 2);
	if (property && strcmp(property, "n") == 0) {
		lua_pushinteger(L, foo->n);
		return 1;
	}
	luaL_error(L, "unknown property");
}

int Foo_newindex(lua_State* L) {
	Foo* foo = static_cast<Foo*>(luaL_touserdatatagged(L, 1, kFooTag));
	const char* property = lua_tostring(L, 2);
	if (property && strcmp(property, "n") == 0) {
		int new_n = luaL_checkinteger(L, 3);
		foo->n = new_n;
		return 0;
	}
	luaL_error(L, "unknown property");
}

const luaL_Reg Foo_metatable[] = {
	{"__index", Foo_index},
	{"__newindex", Foo_newindex},
	{nullptr, nullptr},
};

int push_Foo() {
	Foo* foo = static_cast<Foo*>(lua_newuserdatataggedwithmetatable(L, sizeof(Foo), kFooTag));
	foo->n = 0;
	return 1;
}

// Called during some initialization period
void setup() {
	luaL_newmetatable(L, "Foo");
	luaL_register(L, nullptr, Foo_metatable);
	lua_setuserdatametatable(L, kFooTag);

	lua_setglobal("new_foo", push_Foo);
}
```

```lua
local foo = new_foo()
foo.n = 55
print(foo.n) -- 55
```
