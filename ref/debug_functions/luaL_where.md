---
name: luaL_where
ret: void
stack: "-0, +1, -"
args:
  - name: L
    type: lua_State*
    desc: Lua thread
  - name: level
    type: int
    desc: Stack level
---

Pushes a string onto the stack containing the short source and current line, e.g. `"some/script.luau:10: "`. This is often used as a prefix for other debug logging information.
