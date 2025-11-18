# Tags

Tags are a simple way to interrogate what "type" of userdata we are dealing with.

## The Problem

Consider the following example. We have two structs, Foo and Bar. These will be our userdata. Let's say we already have code to construct these values from Luau, such as `newFoo()` and `newBar()`.
```cpp title="Userdata structs"
struct Foo {
	char* data;
	size_t data_len;
};

struct Bar {
	int n;
};

int new_foo(lua_State* L) {
	void* foo = lua_newuserdata(L, sizeof(Foo));
	foo->data = nullptr;
	foo->data_len = 0;
	return 1;
}

int new_bar(lua_State* L) {
	void* bar = lua_newuserdata(L, sizeof(Bar));
	bar->n = 0;
	return 1;
}
```

```luau title="Creating userdata from Luau"
local foo = newFoo()
local bar = newBar()
```

Now, let's add a function into the mix. This function wants to take an instance of "Foo" and print out its "data_len" property. However, how can we check if the value is actually Foo? We can at least verify it's a userdata, but nothing much more yet:
```cpp title="Print Foo Data Length"
int print_foo_data_len(lua_State* L) {
	luaL_argexpected(L, lua_isuserdata(L, 1), 1, "userdata");

	// Hoping for the best that the user gave us the right userdata:
	Foo* foo = static_cast<Foo*>(lua_touserdata(L, 1));

	printf("data_len: %zu\n", foo->data_len);
}
```

```luau title="Luau Usage"
printFooDataLen(foo) -- works
printFooDataLen(bar) -- UB, likely to crash our whole program
```

How can we solve this?

## Named Metatables

One solution to this is by using named metatables. When we create our userdata, we can build a metatable using `luaL_newmetatable` and bind it to the userdata. Metatables built in this manner have names. And Luau comes with `luaL_checkudata`, which lets us check to see if we have a matching metatable attached.

Let's change up our Foo and Bar constructor code just a bit:
```cpp title="Named Metatables"
int new_foo(lua_State* L) {
	void* foo = lua_newuserdata(L, sizeof(Foo));
	// ...

	if (luaL_newmetatable(L, "Foo")) {
		// ...populate metatable
	}
	lua_setmetatable(L, -2); // bind metatable to foo

	return 1;
}

int new_bar(lua_State* L) {
	void* bar = lua_newuserdata(L, sizeof(Bar));
	// ...

	if (luaL_newmetatable(L, "Bar")) {
		// ...populate metatable
	}
	lua_setmetatable(L, -2); // bind metatable to bar

	return 1;
}
```

Now we can change our `print_foo_data_len` function to use `luaL_checkudata`. If the value isn't a userdata with the "Foo" metatable attached, an error will be thrown:
```cpp
int print_foo_data_len(lua_State* L) {
	Foo* foo = static_cast<Foo*>(luaL_checkudata(L, 1, "Foo"));
	printf("data_len: %zu\n", foo->data_len);
}
```

```luau title="Luau Usage"
printFooDataLen(foo) -- works
printFooDataLen(bar) -- throws Luau error safely (good!)
```

This solves our initial problem. However, there's a couple performance considerations:

1. Calling `luaL_checkudata` can be expensive. It needs to fetch the metatable from the userdata, attempt to fetch the metatable from the Luau registry, and then compare the two.
2. We have to call `luaL_newmetatable` for each new instance of our userdata. This function is idempodent; it will only create one metatable per provided name. However, it still has to reach into the Luau registry and see if it finds an existing metatable first.

## Tags to the Rescue

Tags allow us to assign an integer to represent our userdata type. This is just an arbitrary number that we choose, which should be unique per userdata type. By using tags, we can now ensure we have the proper userdata type by quickly comparing two numbers. This is much faster than doing hash lookups with `luaL_checkudata`.

Another benefit is that we can create our metatable ahead of time, and then use `lua_newuserdatataggedwithmetatable` (what a long name!) to create our userdata with a given tag and metatable.

First, we need to define our tags per userdata. Note that `0` is the default tag given to userdata, so we will want to avoid `0`.
```cpp title="Tag Definitions"
constexpr int kFooTag = 1;
constexpr int kBarTag = 2;
```

Next, we need to define our metatable ahead of time. This is a function we probably call at the same time that we are opening up our libraries.
```cpp
void setup_foo(lua_State* L) {
	luaL_newmetatable(L, "Foo");
	// ...populate metatable
	lua_setuserdatametatable(L, kFooTag); // bind our metatable to our tag

	// OPTIONAL: If we need a destructor, we can assign that here too
	lua_setuserdatadtor(L, kFooTag, [](lua_State* L, void* ptr) {
		Foo* f = static_cast<Foo*>(ptr);
		// free resources as needed
		delete f->data;
	});
}

// ...same type of code for setting up 'Bar'
```

Now we can change our constructor functions to automatically set our tag and metatable:
```cpp
int new_foo(lua_State* L) {
	Foo* foo = static_cast<Foo*>(lua_newuserdatataggedwithmetatable(L, sizeof(Foo), kFooTag));
	foo->data = nullptr;
	foo->data_len = 0;
	// Note how we no longer have to put code here to create and bind the metatable (it's already done!)
	return 1;
}
```

Finally, we can now quickly check that we have the correct userdata by interrogating the tag.

```cpp
// The "lua_touserdatatagged" function returns NULL if our value isn't correct. But we
// want to throw an error. So we'll add this helper function for asserting the userdata:
static Foo* check_foo(lua_State* L, int idx) {
	Foo* foo = static_cast<Foo*>(lua_touserdatatagged(L, idx, kFooTag));
	luaL_argcheck(L, foo, idx, "expected Foo");
	return foo;
}

int print_foo_data_len(lua_State* L) {
	Foo* foo = check_foo(L, 1);
	printf("data_len: %zu\n", foo->data_len);
}
```

By using tags, we:

1. Ensure that we are casting userdata to the correct type
1. Speed up construction of userdata, since we assign the metatable and destructor ahead of time
1. Speed up checking the userdata type, since we only need to compare numeric tags rather than fetch and compare metatables

## Final Notes

### Max Tags

As of writing this, Luau has a tag limit of 128 (including 0, so technically 127 slots available). This is defined by the `LUA_UTAG_LIMIT` constant.

### Sharing Tags

An easy way to keep your tags organized is by creating a single header file that defines each tag. And as a simple reminder of the limit, it is nice to start at the max tag number and count down.

```cpp
// userdata_tags.h
#pragma once

constexpr int kFooTag = 127;
constexpr int kBarTag = 126;
constexpr int kBazTag = 125;
// ...
```
