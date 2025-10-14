---
name: lua_pushvfstring
ret: const char*
stack: "-0, +1, -"
args:
  - name: L
    type: lua_State*
    desc: Lua thread
  - name: fmt
    type: const char*
    desc: C-style string for formatting
  - name: argp
    type: va_list
    desc: Format arguments
---

Pushes a string to the stack, where the string is `fmt` formatted against the arguments in `argp`. The formatted string is also returned.

```cpp title="Example"
void format_something(lua_State* L, const char* fmt, ...) {
	va_list args;
	va_start(args, fmt);
	lua_pushvfstring(L, fmt, args);
	va_end(args);
}

format_something(L, "number: %d", 32);
```
