# Atoms

## The Problem

Consider a method handler that has to deal with multiple different methods. Luau gives us the string of the method, and then we compare the string against all the possible methods. The same scenario can be played out for handling read/write indexing.

```cpp
struct Foo {};

static int Foo_namecall(lua_State* L) {
	const char* method = lua_namecallatom(L, nullptr);

	if (strcmp(method, "DoThis") == 0) {
		// ...
		return 0;
	}
	if (strcmp(method, "DoThat") == 0) {
		// ...
		return 0;
	}
	if (strcmp(method, "RemoveThis") == 0) {
		// ...
		return 0;
	}
	if (strcmp(method, "RemoveThat") == 0) {
		// ...
		return 0;
	}
	// ...
}
```

Our `strcmp` chain is not very efficient. A better way would be something similar to our [Tags](tags.md) solution. Atoms are similar to tags, as they allow us to assign a number per unique string. Luau already interns strings, so Luau is capable of attaching other metadata to those strings, e.g. atoms.

## What is an Atom?

An atom is an integer (`int16_t`). That's it! We can assign this integer to strings via a callback, and then we can inspect this integer with special string functions which include the atom.

## How to Use Atoms

The `lua_callbacks` function allows us to install a `useratom` callback. This callback gets called for any string without an assigned atom that is fetched through a function that also returns an atom, e.g. `lua_namecallatom` and `lua_tostringatom`. In other words, if you call `lua_namecallatom` and provide the `atom` argument, Luau will first call the `useratom` callback if there is no atom assigned, and then will write the atom to your `atom` argument.

```cpp title="Fetching Atom"
static int Foo_namecall(lua_State* L) {
	int atom;
	const char* method = lua_namecallatom(L, &atom);
	// ...
}
```

If no `useratom` callback is installed, then the atom will always be `-1`. Although atoms are written back as `int` types, atoms are internally stored as `int16_t`, so we can assign any value in the range of `[-32768, 32767]`. However, do not use the value of `ATOM_UNDEF` (which currently is set to the minimum value, `-32768`), as Luau will treat that as an unset atom and call the `useratom` callback again for the string.

Let's install a simple `useratom` callback for demonstration purposes. In a real-life scenario, it is probably better to compile some sort of lookup list ahead of time.

```cpp title="Atoms"
// my_atoms.h
constexpr int16_t kAtomDoThis = 1;
constexpr int16_t kAtomDoThat = 2;
constexpr int16_t kAtomRemoveThis = 3;
constexpr int16_t kAtomRemoveThat = 4;
```

```cpp title="Useratom Callback"
#include "my_atoms.h"

static int16_t handle_useratom(const char* s, size_t l) {
	// Match the string to the desired atom value:
	if (strcmp(s, "DoThis") == 0) {
		return kAtomDoThis;
	}
	if (strcmp(s, "DoThat") == 0) {
		return kAtomDoThat;
	}
	if (strcmp(s, "RemoveThis") == 0) {
		return kAtomRemoveThis;
	}
	if (strcmp(s, "RemoveThat") == 0) {
		return kAtomRemoveThat;
	}

	// If our list is dynamically changing, and we want Luau to
	// call this atom handler again for the same string, then we
	// should return `ATOM_UNDEF`. Otherwise, for static lists,
	// just return whatever value you want to use to indicate
	// that no atom was found, but DON'T return `ATOM_UNDEF`:
	return -1;
}

// Call this during our initial state setup
void install_atom_callback(lua_State* L) {
	lua_callbacks(L)->useratom = handle_useratom;
}
```

Now we can modify our `Foo_namecall` function to utilize the atoms instead of a bunch of `strcmp` calls. Simple integer comparisons will perform much better.

```cpp
#include "my_atoms.h"

static int Foo_namecall(lua_State* L) {
	int atom;
	const char* method = lua_namecallatom(L, &atom);

	if (atom == kAtomDoThis) {
		// ...
		return 0;
	}
	if (atom == kAtomDoThat) {
		// ...
		return 0;
	}
	if (atom == kAtomRemoveThis) {
		// ...
		return 0;
	}
	if (atom == kAtomRemoveThat) {
		// ...
		return 0;
	}
	// ...
}
```

To reiterate, the `useratom` callback is only invoked when both of these conditions are met:

1. An atom-fetching function is called with the provided atom callback, e.g. `lua_namecallatom(L, &atom)`
1. The string has yet to have the `useratom` function called on it (i.e. its atom is currently `ATOM_UNDEF`)

If Luau attempts to fetch a string atom _before_ the `useratom` callback is installed, then the atom will be set to `-1`. Thus, ensure that you are installing the callback during your initial setup, before any Luau code is run.

As of writing this, the Luau `lua.h` header file incorrectly states that the `useratom` function gets called when a string is created. This is _not_ true. This _was_ the old behavior, but was [later changed](https://github.com/luau-lang/luau/pull/592) in release 0.536.
