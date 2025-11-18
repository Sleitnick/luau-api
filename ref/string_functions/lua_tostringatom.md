---
name: lua_tostringatom
ret: const char*
stack: "-0, +0, m"
args:
  - name: L
    type: lua_State*
    desc: Lua thread
  - name: idx
    type: int
    desc: Stack index
  - name: atom
    type: int*
    desc: Atom
---

Identical to [`lua_tostring`](#lua_tostring), except the string atom is written to the `atom` argument. See the [Atoms](guides/atoms.md) page for more information on string atoms.
