# FFlags

Luau has a slew of fast flags (FFlags) which can be configured from code. FFlags are scattered about Luau.
If you come across one that you would like to toggle, you can do so with the `LUAU_FASTFLAG` and `LUAU_FASTINT`
macros. These macros inject an `extern` variable pointing to the desired fast flag.

## Example

### Boolean Flag

In Luau version 0.711, Luau added some new math constants, such as `tau` and `phi`. In order for your embedded
version of Luau to add these constants to the `math` library, you need to turn on the `LuauNewMathConstantsRuntime`
flag. This needs to be done prior to opening up the math library.

```cpp
// The Common header includes the necessary macros:
#include <Luau/Common.h>

// Get access to the appropriate fast flag:
LUAU_FASTFLAG(LuauNewMathConstantsRuntime);

void setup() {
	// Set the flag on:
	FFlag::LuauNewMathConstantsRuntime.value = true;

	// ...open Luau state and libraries
}
```

### Integer flag

Alongside fast flags, there are also fast ints. An example of a fast int is `LuauRecursionLimit`. As of writing this,
the limit is set to 1000. Let's set it to 800 instead.

```cpp
LUAU_FASTINT(LuauRecursionLimit);

void setup() {
	FInt::LuauRecursionLimit.value = 800;
}
```

## Custom Flags

Using the `LUAU_FASTFLAGVARIABLE` and `LUAU_FASTINTVARIABLE` macros, you can create your own fast flags.

```cpp
LUAU_FASTFLAGVARIABLE(MyFeature, true);
LUAU_FASTINTVARIABLE(SomeLimit, 12);

void foo() {
	if (FFlag::MyFeature) {
		// Do something
	}

	doSomethingWithLimit(FInt::SomeLimit);
}
```

Other code can then use `LUAU_FASTFLAG(MyFeature)` and `LUAU_FASTINT(SomeLimit)` to get a reference to the flags elsewhere.
