# Threads

Concurrency in Luau is achieved via coroutine threads. Unlike traditional multithreading, Luau "threads" are executed one at a time. The important aspect about coroutines is that they can yield their execution at any time, and can be resumed later. Coroutines are capable of communication too: a coroutine can be given information on startup and during resumptions, and can also yield back information.

The term "coroutine" and "thread" will be used interchangeably throughout this guide. They are both used in reference to Luau's coroutine-type threads. The term "OS thread" will be used to indicate a more traditional operating system thread, typically used in 

Some possible use-cases for coroutines in Luau:
- Running multiple independent scripts without waiting for each other
- Creating a task scheduler
- Allowing a thread to yield while another OS thread performs some work (e.g. yielding for a web request that is running on a separate OS thread)

## Creating Threads

The top global state (e.g. calling `lua_newstate()`) is a `lua_State` object. Threads are _also_ `lua_State` objects. Thus, coroutine threads can be thought of as sub-states of sorts. However, they all belong to the top-level main state (which an be retrieved using `lua_mainstate()`). Threads can communicate with each other as long as they share the same main state.

To create a new thread, call `lua_newthread(L)`, where `L` is the parent thread.

```cpp
lua_State* T = lua_newthread(L);
```

This also pushes the new thread to the top of the stack for `L`.

??? note "Preventing GC"
	Luau threads are subject to being garbage-collected. A common mistake is to hold onto `T` in your code, but remove it from Luau's scope (e.g. popping it from `L` right away), eventually leading to a crash due to `T` being collected. If it doesn't make sense for `L` to hold onto `T` for the duration of `T`s lifetime, then `T` needs to be "pinned" somehow. A common way to do this is by calling `lua_ref`. For more info, see the [Pinning](pinning.md) guide.

## Preparing Threads

TODO

## Sandboxing

TODO (ONLY IF IT'S A 'SCRIPT' PROBABLY)
