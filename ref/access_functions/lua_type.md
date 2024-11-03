---
name: lua_type
ret: int
stack: "-0, +0, -"
args:
  - name: L
    type: lua_State*
    desc: Lua thread
  - name: idx
    type: int
    desc: Stack index
---

Returns the value type at the given stack index. If the stack index is invalid, this function returns `LUA_TNONE`.

List of lua types:

- `LUA_TNIL`
- `LUA_TBOOLEAN`
- `LUA_TLIGHTUSERDATA`
- `LUA_TNUMBER`
- `LUA_TVECTOR`
- `LUA_TSTRING`
- `LUA_TTABLE`
- `LUA_TFUNCTION`
- `LUA_TUSERDATA`
- `LUA_TTHREAD`
- `LUA_TBUFFER`
