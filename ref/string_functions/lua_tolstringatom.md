---
name: lua_tolstringatom
ret: const char*
stack: "-0, +0, m"
args:
  - name: L
    type: lua_State*
    desc: Lua thread
  - name: idx
    type: int
    desc: Stack index
  - name: len
    type: size_t
    desc: String length
  - name: atom
    type: int*
    desc: Atom
---

Identical to [`lua_tolstring`](#lua_tolstring), except the string atom is written to the `atom` argument. See the [Atoms](guides/atoms.md) page for more information on string atoms.
