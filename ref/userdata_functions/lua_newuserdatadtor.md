---
name: lua_newuserdatadtor
ret: void*
stack: "-0, +1, -"
args:
  - name: L
    type: lua_State*
    desc: Lua thread
  - name: sz
    type: size_t
    desc: Size of the data
  - name: dtor
    type: void (*dtor)(void*)
    desc: Destructor
    fn: true
---

Creates a new userdata with an assigned destructor. Destructors are called when Luau is freeing up the userdata memory.

To assign a destructor for all userdata of a given tag, use [`lua_setuserdatadtor`](#lua_setuserdatadtor).

```cpp title="Example" hl_lines="5-9"
struct Foo {
	char* data;
};

Foo* foo = static_cast<Foo*>(lua_newuserdatadtor(L, sizeof(Foo), [](void* ptr) {
	// This function is called when Foo is being GC'd. Free up any user-managed resources now.
	Foo* f = static_cast<Foo*>(ptr);
	delete[] f->data;
}));

foo->data = new char[256];
```
