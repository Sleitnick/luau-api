# Pinning and References

## What is Pinning?

Pinning is a process of forcing a piece of memory from moving or being deleted. In garbage-collected languages, the GC may move memory around for efficiency, and will also decide when to free the memory. In other words, the language is managing the memory.

Luau is a memory-managed language. As such, the Luau GC has control of how memory is allocated, where it goes, and when it's freed. When working with data within Luau _outside_ of its memory domain (e.g. within another language, memory-managed or not), we need to take special care of not accidentally using a piece of memory that vanishes. Luau won't move memory around, so we don't need to worry about the state of our pointers to userdata or buffers, but we do need to worry abou Luau deciding to free up memory. Therefore, when we talk about "pinning" with Luau objects, what we really mean is, "don't delete this."

Luau can only keep track of what exists within its domain. If you pull a value out of its domain, Luau has no way of knowing about it. Thus, the GC may determine there are no more references to the object _within its known domain_, and then delete it.

If we want to keep Luau from freeing a value, we need a way to tell Luau, "Hey, please don't free this value while I'm holding onto it." There are a few ways to do this.

## Pinning on the Stack

One method of pinning is leaving a value on the stack. Of course, this has to be on the stack of a Luau thread that is also referenced elsewhere too (all values in Luau, including threads, are subject to being GC'd).

You may already be doing this without realizing it. For instance, we keep new threads alive by keeping them on the stack where they were created until the thread is done. Failing to do so (i.e. popping it early) may result in the thread being GC'd and causing lots of fun problems.

```cpp
lua_State* T = lua_newthread(L); // T is pushed to the stack of L (not going anywhere!)

// ...push some function onto T, and maybe some args
int status = lua_resume(T, nullptr, 0);
// ...handle status

lua_pop(L, 1); // Pop T from L. We no longer need it pinned. The GC is free to pick up T now.
```

## Pinning within a Table

We can also pin a value by placing it into a table. This table also has to live somewhere that won't get GC'd either. We could create a table within the Luau registry and place our values there.

```cpp
// store a ref
void set_ref(lua_State* L, const char* name, int idx) {
	idx = lua_absindex(idx);
	luaL_findtable(L, LUA_REGISTRYINDEX, "references");
	lua_pushvalue(L, idx);
	lua_rawsetfield(L, -2, name); // references[name] = stack[idx]
	lua_pop(L, 1); // pop 'references' table
}

// push value of ref to stack
void get_ref(lua_State* L, const char* name) {
	luaL_findtable(L, LUA_REGISTRYINDEX, "references");
	lua_rawgetfield(L, -1, name);
	lua_remove(L, -2); // pop 'references' table
}

// delete a ref
void clear_ref(lua_State* L, const char* name) {
	lua_pushnil(L);
	set_ref(L, name, -1);
	lua_pop(L, 1);
}

// Test:
struct Foo {};
lua_pushuserdata(L, sizeof(Foo));
set_ref(L, "foo", -1);
lua_pop(L, 1); // pop userdata

get_ref(L, "foo");
Foo* foo = static_cast<Foo*>(lua_touserdata(L, -1));

clear_ref(L, "foo");
```

Well, that's a lot of work. And we could have skipped a lot of that by writing directly to the LUA_REGISTRYINDEX table anyway. But it's not very flexible for dynamic references, as we need a defined name per reference. What if we have a dynamic number of objects that all need their own reference?

## Pinning with lua_ref

Luau comes with a nifty reference system built-in. All we need to do is call `lua_ref` and it will hand us an integer as a reference to the object. Internally, this is storing the values within the Luau registry. We can call `lua_unref` to remove our reference and `lua_getref` to retrieve the value.

By creating a reference to our object, we are inherently pinning the value. We can also create multiple references for a single object. Because this is storing the value within the Luau registry, the GC sees the value and won't delete it.

So, in order to pin our desired value, we just need to use the built-in reference system.

```cpp
struct Foo {};
lua_pushuserdata(L, sizeof(Foo));
int foo_ref = lua_ref(L, -1);
lua_pop(L, 1); // pop userdata

lua_getref(L, foo_ref);
Foo* foo = static_cast<Foo*>(lua_touserdata(L, -1));

lua_unref(L, foo_ref);
```

## RAII and Shared Pointers

Because `lua_ref` requires us to call `lua_unref` to free the reference, we can easily end up with the same memory leak bugs that plague unmanaged-memory languages. However, we can utilize modern concepts and features to help us out. Using shared pointers and RAII, we can easily encapsulate Luau references in a safer manner.

```cpp
// This is just a bare-bones example.
// Based on Lute's 'Ref' class: https://github.com/luau-lang/lute/blob/primary/lute/runtime/src/ref.cpp

class LuauRef {
private:
	int ref = LUA_NOREF;
	lua_State* main;

public:
	LuauRef(lua_State* L, int idx) {
		ref = lua_ref(L, idx);
		main = lua_mainthread(L);
	}

	~LuauRef() {
		lua_unref(main, ref);
	}

	// Push the value of the reference to the stack
	void push(lua_State* L) {
		lua_getref(L, ref);
	}
};

// Using shared_ptr with LuauRef:
lua_newuserdata(L, sizeof(Foo));
std::shared_ptr<LuauRef> ref = std::make_shared<LuauRef>(L, -1);
lua_pop(L, 1);

// Now we can pass "ref" around safely and retain our reference to our Foo userdata.
// We can retrieve the value by calling 'push':
ref->push(L);
Foo* foo = static_cast<Foo*>(lua_touserdata(L, -1));
```
