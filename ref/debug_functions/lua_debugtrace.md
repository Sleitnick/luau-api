---
name: lua_debugtrace
ret: const char*
stack: "-0, +0, -"
args:
  - name: L
    type: lua_State*
    desc: Lua thread
---

Gets a traceback string.

**Note:** Internally, this uses a static string buffer. Thus, this function is not thread-safe, nor is it safe to hold onto the returned value. Create a copy of the returned string if needed.
