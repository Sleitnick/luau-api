---
name: lua_concat
ret: void
stack: "-n, +1, -"
args:
  - name: L
    type: lua_State*
    desc: Lua thread
  - name: n
    type: int
    desc: Number of values
---

Performs string concatenation on the `n` values on the top of the stack. All `n` values are popped, and the resultant string is pushed to the stack. If `n` is `1`, this function does nothing. If `n` is `0`, an empty string is pushed to the stack. For all other values of `n` (assuming >= 2), all values are popped and concatenated into a string.
