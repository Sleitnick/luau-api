---
name: lua_tonumberx
ret: double
stack: "-0, +0, -"
args:
  - name: L
    type: lua_State*
    desc: Lua thread
  - name: idx
    type: int
    desc: Stack index
  - name: isnum
    type: int*
    desc: Is number
---

Returns the number at the given stack index. If the value on the stack is a string, Luau will attempt to convert the string to a number.

If the value is a number, or successfully converted to a number, the `isnum` argument will be set to `1`, otherwise `0`.

```cpp title="Example" hl_lines="9 15 21"
lua_pushliteral(L, "hello");
lua_pushliteral(L, "12.5");
lua_pushnumber(L, 15);

double n;
int isnum;

// isnum will be false, since "hello" cannot be converted to a number:
n = lua_tonumberx(L, -3, &isnum);
if (isnum) {
	printf("n: %f\n", n);
}

// isnum is true, and "12.5" is converted to 12.5:
n = lua_tonumberx(L, -2, &isnum);
if (isnum) {
	printf("n: %f\n", n);
}

// isnum is true, and the value is 15:
n = lua_tonumberx(L, -1, &isnum);
if (isnum) {
	printf("n: %f\n", n);
}
```
