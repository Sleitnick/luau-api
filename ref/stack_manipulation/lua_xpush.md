---
name: lua_xpush
ret: void
stack: "-0, +1, -"
args:
  - name: from
    type: lua_State*
    desc: Lua thread
  - name: to
    type: lua_State*
    desc: Lua thread
  - name: idx
    type: int
    desc: Stack index
---

Pushes a value from the `from` state to the `to` state. The value at index `idx` in `from` is pushed to the top of the `to` stack. This is similar to `lua_pushvalue`, except the value is pushed to a different state.

Similar to `lua_xmove`, both `from` and `to` must share the same global state.

```cpp title="Example"
// Push the value at index -2 within 'from' to the top of the 'to' stack:
lua_xpush(from, to, -2);
```
