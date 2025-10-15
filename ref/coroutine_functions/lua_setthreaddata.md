---
name: lua_setthreaddata
ret: void
stack: "-0, +0, -"
args:
  - name: L
    type: lua_State*
    desc: Lua thread
---

Sets arbitrary data for a given thread. This is often useful when using lua interrupt or thread callbacks (see [`lua_callbacks`](#lua_callbacks)).

This value ought not be a Luau-owned object (e.g. data created with `lua_newuserdata`), since the lifetime of that memory may be shorter than the lifetime of the given thread.

```cpp title="Example"
class Foo {};

lua_setthreaddata(L, new Foo());
// ...
Foo* foo = static_cast<Foo*>(lua_getthreaddata(L));
// ...
lua_setthreaddata(L, nullptr);
delete foo;
```
