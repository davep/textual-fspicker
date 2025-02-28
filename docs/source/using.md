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
from textual_fspicker import FileSave

...

class SomeApp(App):

   ...

   @on(Button.Clicked, "#save")
   @work
   async def save_document(self) -> None:
       """Save the document."""
       if save_to := await self.push_screen_wait(FileSave()):
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
[`default_file`][textual_fspicker.FileOpen] keyword parameter:

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

### Ensuring the file exists

A user can select a file by either picking one from the directory navigation
widget within the dialog, or by typing the path and name of a file in the
[`Input`][textual.widgets.Input] widget in the dialog. If they type in a
name it's possible for them to type in the name of a file that doesn't
exist.

In such a case the dialog will refuse to close and an error will be shown:

```{.textual path="docs/examples/guide/basic_open_file.py" press="enter,tab,b,a,d,.,p,y,enter"}
```

If you want the allow the user to "open" a file that doesn't really exist,
in other words you want them to be able to type in any name they wish, you
can set the [`must_exist`][textual_fspicker.FileOpen] keyword parameter to
[`False`][False]:

=== "Allowing files that don't exist"

    ```py
    --8<-- "docs/examples/guide/any_open_file.py"
    ```

=== "Initially"

    ```{.textual path="docs/examples/guide/any_open_file.py"}
    ```

=== "Dialog Open"

    ```{.textual path="docs/examples/guide/any_open_file.py" press="enter"}
    ```

=== "File Entered"

    ```{.textual path="docs/examples/guide/any_open_file.py" press="enter,tab,b,a,d,.,p,y"}
    ```

=== "File Picked"

    ```{.textual path="docs/examples/guide/any_open_file.py" press="enter,tab,b,a,d,.,p,y,enter"}
    ```

## Saving a file

The [`FileSave`][textual_fspicker.FileSave] dialog is used to prompt the
user for file to save. The most basic example looks like this:

=== "Basic file saving example"

    ```py
    --8<-- "docs/examples/guide/basic_save_file.py"
    ```

=== "Initially"

    ```{.textual path="docs/examples/guide/basic_save_file.py"}
    ```

=== "Dialog Open"

    ```{.textual path="docs/examples/guide/basic_save_file.py" press="enter"}
    ```

=== "File Picked"

    ```{.textual path="docs/examples/guide/basic_save_file.py" press="enter,down,down,down,down,down,enter,enter"}
    ```
### Setting the default file

When prompting for a file to save to, you may want to specify a default
filename which will be shown to the user when the dialog opens; this can be
done with the [`default_file`][textual_fspicker.FileSave] keyword parameter:

=== "Saving with a default file"

    ```py
    --8<-- "docs/examples/guide/default_save_file.py"
    ```

=== "Initially"

    ```{.textual path="docs/examples/guide/default_save_file.py"}
    ```

=== "Dialog Save"

    ```{.textual path="docs/examples/guide/default_save_file.py" press="enter"}
    ```

=== "File Picked"

    ```{.textual path="docs/examples/guide/default_save_file.py" press="enter,tab,enter"}
    ```

### Preventing overwrite of an existing file

When it comes to picking a file to save to, the user can either select a
pre-existing file, or they can enter the name of a new file. Sometimes you
may want to use this dialog to prompt them for a file to save to, but you
want to prevent them from overwriting an existing file. This can be done
with the [`can_overwrite`][textual_fspicker.FileSave] parameter. If set to
[`False`][False] the dialog will refuse to close while an existing file is
selected:

=== "Preventing overwrite of a file"

    ```py
    --8<-- "docs/examples/guide/no_overwrite_save_file.py"
    ```

=== "Overwrite disallowed error"

    ```{.textual path="docs/examples/guide/no_overwrite_save_file.py" press="enter,down,down,down,down,down,enter,enter"}
    ```

## Picking a directory

The [`SelectDirectory`][textual_fspicker.SelectDirectory] dialog is used to
prompt the user for a directory. The most basic example looks like this:

=== "Basic directory picking example"

    ```py
    --8<-- "docs/examples/guide/basic_select_directory.py"
    ```

=== "Initially"

    ```{.textual path="docs/examples/guide/basic_select_directory.py"}
    ```

=== "Dialog Open"

    ```{.textual path="docs/examples/guide/basic_select_directory.py" press="enter"}
    ```

=== "Directory picked"

    ```{.textual path="docs/examples/guide/basic_select_directory.py" press="enter,down,down,enter,tab,enter"}
    ```

## Filtering

The [`FileOpen`][textual_fspicker.FileOpen] and
[`FileSave`][textual_fspicker.FileSave] dialogs have an optional filter
facility; this displays as a [Textual `Select`][textual.widgets.Select]
widget within the dialog and provides the user with a list of prompts that
can filter down the content of the dialog.

For example:

```{.textual path="docs/examples/guide/filter_open.py" lines=30 columns=100 press="tab,tab,enter"}
```

The filters are passed to either dialog using the `filters` keyword
argument, the value being a [`Filters`][textual_fspicker.Filters] object.
`Filters` takes as its parameters a series of [tuples][tuple], each
comprising of a [string][str] label and a function that takes a
[`Path`][pathlib.Path] and returns a [`bool`][bool]. For any given function,
if it returns `True` the file will be included in the display, if `False` it
will be filtered out.

The code for the dialog shown above would look something like this:

```python
FileOpen(
    filters=Filters(
        ("Python", lambda p: p.suffix.lower() == ".py"),
        ("Markdown", lambda p: p.suffix.lower() == ".md"),
        ("TOML", lambda p: p.suffix.lower() == ".toml"),
        ("YAML", lambda p: p.suffix.lower() == ".yaml"),
        ("All", lambda _: True),
    )
)
```

[//]: # (using.md ends here)
