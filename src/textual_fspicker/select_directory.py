"""Provides a directory selection dialog."""

##############################################################################
# Backward compatibility.
from __future__ import annotations

##############################################################################
# Python imports.
from pathlib import Path

##############################################################################
# Textual imports.
from textual import on
from textual.app import ComposeResult
from textual.reactive import var
from textual.widgets import Button, Label, Input

##############################################################################
# Local imports.
from .base_dialog import ButtonLabel, FileSystemPickerScreen
from .parts import DirectoryNavigation
from .path_maker import MakePath


##############################################################################
# class CurrentDirectory(Label): # MODIFIED: This class will be replaced by an Input
#     """A widget to show the current directory.
#
#     This widget is used inside a
#     [`SelectDirectory`][textual_fspicker.SelectDirectory] dialog to display
#     the currently-selected directory.
#     """
#
#     DEFAULT_CSS = """
#     CurrentDirectory {
#         width: 1fr;
#         height: 3; /* Input default height is 3, so this might be fine */
#         border: tall $background;
#         padding-left: 1;
#         padding-right: 1;
#     }
#     """
#
#     current_directory: var[Path | None] = var(None, always_update=True)
#     """The current directory."""
#
#     def _watch_current_directory(self) -> None:
#         """Watch for the current directory being changed."""
#         if (
#             len(
#                 display := ""
#                 if self.current_directory is None
#                 else str(self.current_directory)[-self.size.width :]
#             )
#             >= self.size.width
#         ):
#             display = f"…{display[1:]}"
#         self.update(display)
#
#     def _on_resize(self) -> None:
#         self.current_directory = self.current_directory


##############################################################################
class SelectDirectory(FileSystemPickerScreen):
    """A directory selection dialog."""

    DEFAULT_CSS = FileSystemPickerScreen.DEFAULT_CSS + """
    SelectDirectory InputBar {
        Input { /* Style for the new path input */
            width: 2fr; /* Give it more space than buttons */
            margin-right: 1;
        }
    }
    """

    def __init__(
        self,
        location: str | Path = ".",
        title: str = "Select directory",
        *,
        select_button: ButtonLabel = "",
        cancel_button: ButtonLabel = "",
    ) -> None:
        """Initialise the dialog.

        Args:
            location: Optional starting location.
            title: Optional title.
            select_button: The label for the select button.
            cancel_button: The label for the cancel button.

        Notes:
            `select_button` and `cancel_button` can either be strings that
            set the button label, or they can be functions that take the
            default button label as a parameter and return the label to use.
        """
        super().__init__(
            location, title, select_button=select_button, cancel_button=cancel_button
        )

    def on_mount(self) -> None:
        """Configure the dialog once the DOM is ready."""
        super().on_mount() # Call parent's on_mount
        navigation = self.query_one(DirectoryNavigation)
        navigation.show_files = False

        path_input = self.query_one("#path_input", Input)
        path_input.value = str(navigation.location)
        # navigation.focus() # Focus is handled by super().on_mount or should be reconsidered

    def _input_bar(self) -> ComposeResult:
        """Provide any widgets for the input before, before the buttons."""
        # MODIFIED: Yield an Input widget instead of CurrentDirectory
        yield Input(id="path_input", placeholder="Type path or select below")

    @on(DirectoryNavigation.Changed)
    def _update_path_input_on_nav_change(self, event: DirectoryNavigation.Changed) -> None:
        """Update the display of the current location in the Input widget.

        Args:
            event: The event with the selection information in.
        """
        # This combines the original _show_selected from SelectDirectory
        # and the _on_directory_changed from FileSystemPickerScreen
        # We need to ensure error clearing and path label (if kept separate) update happen.
        # For now, the main path label is in FileSystemPickerScreen.
        # This handler is specific to SelectDirectory's path_input.

        super()._on_directory_changed(event) # Call parent handler for main path label and error clearing
        event.stop() # Stop event propagation if necessary, depending on desired interactions
        path_input = self.query_one("#path_input", Input)
        path_input.value = str(event.control.location)

    @on(Input.Submitted, "#path_input")
    def _handle_path_input_submission(self, event: Input.Submitted) -> None:
        """Handle submission of the path Input widget."""
        event.stop()
        path_value = event.value
        dir_nav = self.query_one(DirectoryNavigation)
        try:
            # Attempt to resolve the path
            target_path = MakePath.of(path_value).expanduser().resolve()
            if target_path.is_dir():
                dir_nav.location = target_path # This will trigger DirectoryNavigation.Changed
                # dir_nav.focus() # Optionally refocus directory navigation
            else:
                self._set_error(f"Not a directory: {target_path.name}")
                self.query_one("#path_input", Input).focus()
        except FileNotFoundError:
            self._set_error(f"Path not found: {path_value}")
            self.query_one("#path_input", Input).focus()
        except PermissionError:
            self._set_error(self.ERROR_PERMISSION_ERROR)
            self.query_one("#path_input", Input).focus()
        except RuntimeError as e: # For MakePath.expanduser() issues
            self._set_error(str(e))
            self.query_one("#path_input", Input).focus()


    @on(Button.Pressed, "#select")
    def _select_directory(self, event: Button.Pressed) -> None:
        """React to the select button being pressed.

        Args:
            event: The button press event.
        """
        event.stop()
        # The location in DirectoryNavigation is the source of truth,
        # whether set by list interaction or by the path_input.
        self.dismiss(result=self.query_one(DirectoryNavigation).location)


### select_directory.py ends here
