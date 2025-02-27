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


[//]: # (using.md ends here)
