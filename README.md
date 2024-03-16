# textual-fspicker

![Viewing its own directory](https://raw.githubusercontent.com/davep/textual-fspicker/main/img/textual-fspicker.png)
*An example of `textual-fspicker` being used in a Textual application*

## Introduction

This library provides a simple set of filesystem navigation and picking
dialogs (actually, as of the time of writing, it only provides two, this is
a very early WiP you're seeing). The aim is to provide "ready to go" dialogs
that should also be fairly easy to tailor to your own applications.

## Installing

The package can be installed with `pip` or related tools, for example:

```sh
$ pip install textual-fspicker
```

## The library

Right at the moment there's just two dialogs available:

- `FileOpen` -- For selecting a file from the filesystem.
- `FileSave` -- For selecting a file for saving in the filesystem.
- `SelectDirectory` -- For selecting a directory from the filesysrem.

You can see them in action in the [demo/test
code](https://github.com/davep/textual-fspicker/blob/main/textual_fspicker/__main__.py).

Yes, I know that documentation is lacking right now -- I'm still fleshing
out how this will work and what it will provide -- so the best place to see
how the code can be used is in that demo/test code.

## TODO

- [ ] Flesh out what's displayed for directory entries
- [ ] Add lots of styling options for directory entries
- [ ] Settle on a final set of default styles for the dialogs
- [X] Add a more file-save-oriented dialog
- [X] Add a directory picking dialog
- [X] Add file filtering (extensions using `Select`)
- [X] Expose the hidden show/hide facility of the navigator in the dialogs
- [ ] Better documentation
- [ ] Test on Windows
- [ ] Add custom mtime formatting
- [ ] Add support for showing different times

[//]: # (README.md ends here)
