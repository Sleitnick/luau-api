---
name: lua_pushcclosurek
ret: void
stack: "-n, +1, -"
args:
  - name: L
    type: lua_State*
    desc: Lua thread
  - name: fn
    type: lua_CFunction
    desc: C Function
  - name: debugname
    type: const char*
    desc: Debug name
  - name: nup
    type: int
    desc: Number of upvalues to capture
  - name: cont
    type: lua_Continuation
    desc: Continuation function to invoke
---

Pushes the C function to the stack as a closure, which captures and pops `nup` upvalues from the top of the stack. The closure's continuation function is also assigned to `cont`.

The continuation function is invoked when the closure is resumed.

```cpp title="Example" hl_lines="23"
int addition_cont(lua_State* L) {
	double add = lua_tonumber(L, lua_upvalueindex(2)); // 4
	double n = lua_tonumber(L, 1);
	double sum = n + add;
	lua_pushnumber(L, sum);
	// Stop generator if sum exceeds 100 (this would obviously be bad if 'add' was <= 0)
	if (sum > 100) {
		return 1;
	}
	return lua_yield(L, 1);
}

int addition(lua_State* L) {
	double start = lua_tonumber(L, lua_upvalueindex(1)); // 10
	double add = lua_tonumber(L, lua_upvalueindex(2)); // 4
	lua_pushnumber(L, start + add);
	return lua_yield(L, 1);
}

int start_addition(lua_State* L) {
	lua_pushvalue(L, 1);
	lua_pushvalue(L, 2);
	lua_pushcclosurek(L, addition, "addition", 2, addition_cont);
}

// Expose "start_addition" to Luau:
set_global(L, "start_addition", start_addition);
```

```lua
-- Start adder generator from 10 and add by 4:
local adder = coroutine.wrap(start_addition(10, 4))
do
	local sum = adder()
	print(sum)
until not sum
```
