# textual-fspicker

![Viewing its own directory](https://raw.githubusercontent.com/davep/textual-fspicker/main/img/textual-fspicker.png)
*An example of `textual-fspicker` being used in a Textual application*

## Introduction

This library provides a simple set of filesystem navigation and picking
dialogs (actually, as of the time of writing, it only provides the one, this
is a very early WiP you're seeing). The aim is to provide "ready to go"
dialogs that should also be fairly easy to tailor to your own applications.

## Installing

The package can be installed with `pip` or related tools, for example:

```sh
$ pip install textual-fspicker
```

## It's early days

This is a very early release of this code, it's still very much a work in
progress. This means things may change and break; it's also sitting atop
Textual which is, of course, still undergoing rapid development. As much as
possible I'll try and ensure that it's always working with the latest stable
release of Textual.

Also, because it's early days... while I love the collaborative aspect of
FOSS, I'm highly unlikely to be accepting any non-trivial PRs at the moment.
Developing this is a learning exercise for me, it's a hobby project, and
it's also something to help me further test Textual (disclaimer for those
who may not have gathered, I am employed by
[Textualize](https://www.textualize.io/)).

On the other hand: I'm *very* open to feedback and suggestions so don't
hesitate to engage with me in Discussions, or if it's a bug, in Issues. I
can't and won't promise that I'll take everything on board (see above about
hobby project, etc), but helpful input should help make this as useful as
possible in the longer term.

## The library

Right at the moment there's just the one dialog available, which is geared
to getting the path to a file that you'll open. Here's a little example
Textual application that shows using it:

```python
"""Main entry point for testing the library."""

##############################################################################
# Python imports.
from pathlib import Path

##############################################################################
# Textual imports.
from textual.app     import App, ComposeResult
from textual.widgets import Label, Button

##############################################################################
# Local imports.
from textual_fspicker import FileOpen

##############################################################################
class TestApp( App[ None ] ):
    """A simple test application."""

    def compose( self ) -> ComposeResult:
        yield Label( "Press the button to pick something" )
        yield Button( "Select a file" )

    def show_selected( self, to_open: Path ) -> None:
        self.query_one( Label ).update( str( to_open ) )

    def on_button_pressed( self ):
        self.push_screen( FileOpen( "." ), callback=self.show_selected )

##############################################################################
if __name__ == "__main__":
    TestApp().run()

### __main__.py ends here
```

The `FileOpen` dialog has the following parameters:

- `location` - The optional start location.
- `title` - The optional title, defaults to `"Open"`
- `must_exist` - Optional flag to say the chosen file must exist, defaults
  to `True`.

## TODO

- [ ] Flesh out what's displayed for directory entries
- [ ] Add lots of styling options for directory entries
- [ ] Settle on a final set of default styles for the dialogs
- [ ] Add a more file-save-oriented dialog
- [ ] Add a directory picking dialog
- [ ] Add file filtering (extensions using `Select`)
- [ ] Expose the hidden show/hide facility of the navigator in the dialogs
- [ ] Better documentation
- [ ] Test on Windows
- [ ] Add custom mtime formatting
- [ ] Add support for showing different times

[//]: # (README.md ends here)
