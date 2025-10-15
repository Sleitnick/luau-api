---
name: lua_gc
ret: int
stack: "-0, +0, -"
args:
  - name: L
    type: lua_State*
    desc: Lua thread
  - name: what
    type: int
    desc: What
  - name: data
    type: int
    desc: Data
---

Various garbage collection operations, determined by the `what` argument.

Starting and stopping the GC:

- To stop the GC: `lua_gc(L, LUA_GCSTOP, 0);`
- To restart the GC: `lua_gc(L, LUA_GCRESTART, 0);`
- To run a full GC cycle: `lua_gc(L, LUA_GCCOLLECT, 0);`
- To run a GC step: `lua_gc(L, LUA_GCSTEP, 0);`

Querying the GC:

- To check if the GC is running: `if (lua_gc(L, LUA_GCISRUNNING, 0)) {}`
- To count GC usage in kilobytes: `int kb = lua_gc(L, LUA_GCCOUNT, 0);`
- To count the remaining GC in bytes: `int b = lua_gc(L, LUA_GCCOUNTB, 0);`

Tuning the GC:

- To set the GC goal (percentage): `lua_gc(L, LUA_GCSETGOAL, 200);`
- To set the GC step multiplier (percentage): `lua_gc(L, LUA_GCSETSTEPMUL, 200);`
- To set the GC step size (KB): `lua_gc(L, LUA_GCSETSTEPSIZE, 1);`

```cpp title="Example"
// Example of querying bytes used:
int kb = lua_gc(L, LUA_GCCOUNT, 0);
int bytes_remaining = lua_gc(L, LUA_GCCOUNTB, 0);
int bytes_total = (kb * 1024) + byte_remaining;
printf("gc size: %d bytes", bytes_total);
```
