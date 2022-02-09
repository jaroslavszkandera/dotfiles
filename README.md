# Dotfiles

My config files.
I'm currently experimenting with a lot of things.
However, I think you can get inspiration from some of these.

## For CTU students

There are a few paths that might be of interest to you.

### .local/share/Anki2/addons21/

This is the folder with Anki addons I'm currently using.

### .local/scripts/

This is a home of all the scripts.
`do-cpp` will be most interesting to you.
It's a wrapper around `g++`, but with progtest flags and memory debugger enabled.
You can also provide folder with tests in format: *_in.txt* files as input and *_ref.txt* as reference.
To compile file automatically when changed, use `watch-cpp` script.

## Filters

I use local git filters in order to exclude volatile or machine specific stuff in config files.

```[bash]
dfl config filter.pkglist.clean git-filter-pkglist
```
