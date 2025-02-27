# Using the library

## The dialogs

`textual-fspicker` provides three public dialogs: one for selecting a file
for opening, one for selecting a file for saving, and one for selecting a
pre-existing directory. Each dialog is implemented as a [Textual modal
screen](https://textual.textualize.io/guide/screens/#modal-screens).

Each of the dialogs is designed to return a [dismiss
result](https://textual.textualize.io/guide/screens/#returning-data-from-screens)
of the [`Path`][pathlib.Path] of the filesystem entry that was selected, or
[`None`][None] if the user cancelled the dialog.

The usual pattern for using one of the dialogs, using [Textual's ability to
wait for a
screen](https://textual.textualize.io/guide/screens/#waiting-for-screens)
will look something like this:

```python
from textual_fspicker import FileOpen

...

class SomeApp(App):

   ...

   @on(Button.Clicked, "#save")
   @work
   async def save_document(self) -> None:
       """Save the document."""
       if save_to := await self.push_screen_wait(FileOpen()):
           my_saving_function(save_to)
           self.notify("Saved")
       else:
           self.notify("Save cancelled")
```

## Opening a file

The [`FileOpen`][textual_fspicker.FileOpen] dialog is used to prompt the user for file to
open. The most basic example looks like this:

=== "Basic file opening example"

    ```py
    --8<-- "docs/examples/guide/basic_open_file.py"
    ```

=== "Initially"

    ```{.textual path="docs/examples/guide/basic_open_file.py"}
    ```

=== "Dialog Open"

    ```{.textual path="docs/examples/guide/basic_open_file.py" press="enter"}
    ```

=== "File Picked"

    ```{.textual path="docs/examples/guide/basic_open_file.py" press="enter,down,down,down,down,down,enter,enter"}
    ```

### Setting the default file

When opening a file, you may want to specify a default filename which will
be shown to the user when the dialog opens; this can be done with the
`default_file` keyword parameter:

=== "Opening with a default file"

    ```py
    --8<-- "docs/examples/guide/default_open_file.py"
    ```

=== "Initially"

    ```{.textual path="docs/examples/guide/default_open_file.py"}
    ```

=== "Dialog Open"

    ```{.textual path="docs/examples/guide/default_open_file.py" press="enter"}
    ```

=== "File Picked"

    ```{.textual path="docs/examples/guide/default_open_file.py" press="enter,tab,enter"}
    ```

[//]: # (using.md ends here)
