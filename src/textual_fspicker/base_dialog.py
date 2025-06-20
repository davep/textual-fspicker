"""The base dialog code for the other dialogs in the library."""

##############################################################################
# Backward compatibility.
from __future__ import annotations

##############################################################################
# Python imports.
import sys
from pathlib import Path
from typing import Callable, TypeAlias, List, Dict, Any
import json
from datetime import datetime

##############################################################################
# Textual imports.
from textual import on
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, Vertical, VerticalScroll
from textual.screen import ModalScreen
from textual.widgets import Button, Label, Input, ListView, ListItem
from textual.reactive import reactive

##############################################################################
# Local imports.
from .parts import DirectoryNavigation, DriveNavigation


##############################################################################
class Dialog(Vertical):
    """Layout class for the main dialog area."""


##############################################################################
class InputBar(Horizontal):
    """The input bar area of the dialog."""


##############################################################################
ButtonLabel: TypeAlias = str | Callable[[str], str]
"""The type for a button label value."""


##############################################################################
class FileSystemPickerScreen(ModalScreen[Path | None]):
    """Base screen for the dialogs in this library."""

    DEFAULT_CSS = """
    FileSystemPickerScreen {
        align: center middle;

        Dialog {
            width: 80%;
            height: 80%;
            border: $border;
            background: $panel;
            border-title-color: $text;
            border-title-background: $panel;
            border-subtitle-color: $text;
            border-subtitle-background: $error;

            OptionList, OptionList:focus {
                background: $panel;
                background-tint: $panel;
            }
        }

        #current_path_display {
            width: 1fr;
            padding: 0 1;
            margin-bottom: 1;
            overflow: hidden;
            text-overflow: ellipsis;
            color: $text-muted;
        }
        
        #path-breadcrumbs {
            height: 3;
            padding: 1;
            background: $surface;
            margin-bottom: 1;
        }
        
        #path-breadcrumbs Button {
            min-width: 0;
            padding: 0 1;
            margin: 0;
            height: 1;
            background: transparent;
            border: none;
        }
        
        #path-breadcrumbs Button:hover {
            background: $boost;
        }
        
        #clear-search {
            background: $boost;
            border: none;
        }
        
        #path-breadcrumbs .breadcrumb-separator {
            margin: 0 1;
            color: $text-muted;
        }
        
        #search-container {
            height: 3;
            padding: 0 1;
            margin-bottom: 1;
            display: none;
        }
        
        #search-container.visible {
            display: block;
        }
        
        #search-input {
            width: 1fr;
        }

        DirectoryNavigation {
            height: 1fr;
        }

        InputBar {
            height: auto;
            align: right middle;
            padding-top: 1;
            padding-right: 1;
            padding-bottom: 1;
            Button {
                margin-left: 1;
            }
        }
    }
    """

    ERROR_PERMISSION_ERROR = "Permission error"
    """Error to tell there user there was a problem with permissions."""

    BINDINGS = [
        Binding("full_stop", "hidden", "Toggle hidden"),
        Binding("ctrl+h", "hidden", "Toggle hidden files"),
        Binding("ctrl+l", "focus_path_input", "Edit path directly"),
        Binding("f5", "refresh", "Refresh directory"),
        Binding("ctrl+f", "focus_search", "Search in directory"),
        Binding("escape", "dismiss(None)", "Cancel")
    ]
    """The bindings for the dialog."""
    
    search_active = reactive(False)
    """Whether search is active."""
    
    def __init__(
        self,
        location: str | Path = ".",
        title: str = "",
        select_button: ButtonLabel = "",
        cancel_button: ButtonLabel = "",
    ) -> None:
        """Initialise the dialog.

        Args:
            location: Optional starting location.
            title: Optional title.
            select_button: Label or format function for the select button.
            cancel_button: Label or format function for the cancel button.
        """
        super().__init__()
        self._location = location
        """The starting location."""
        self._title = title
        """The title for the dialog."""
        self._select_button = select_button
        """The text prompt for the select button, or a function to format it."""
        self._cancel_button = cancel_button
        """The text prompt for the cancel button, or a function to format it."""

    def _input_bar(self) -> ComposeResult:
        """Provide any widgets for the input bar, before the buttons."""
        yield from ()

    @staticmethod
    def _label(label: ButtonLabel, default: str) -> str:
        """Create a label for use with a button.

        Args:
            label: The label value for the button.
            default: The default label for the button.

        Returns:
            The formatted label.
        """
        # If the label is callable, then call it with the default as a
        # parameter; otherwise use it as-is as it'll be a string.
        return label(default) if callable(label) else label or default

    def compose(self) -> ComposeResult:
        """Compose the child widgets.

        Returns:
            The widgets to compose.
        """
        with Dialog() as dialog:
            dialog.border_title = self._title
            
            # Path display and breadcrumbs
            yield Label(id="current_path_display")
            with Horizontal(id="path-breadcrumbs"):
                # Breadcrumbs will be dynamically populated
                pass
            
            # Path input field (hidden by default, shown with Ctrl+L)
            with Horizontal(id="path-input-container", classes="hidden"):
                yield Input(placeholder="Enter path...", id="path-input")
                yield Button("Go", id="go-to-path", variant="primary")
                yield Button("Cancel", id="cancel-path-input", variant="default")
            
            # Search container (hidden by default)
            with Horizontal(id="search-container"):
                yield Input(placeholder="Search files...", id="search-input")
                yield Button("Clear", id="clear-search", variant="default")
            
            # Main directory navigation
            with Horizontal():
                if sys.platform == "win32":
                    yield DriveNavigation(self._location)
                yield DirectoryNavigation(self._location)
            
            # Input bar with buttons
            with InputBar():
                yield from self._input_bar()
                yield Button(self._label(self._select_button, "Select"), id="select")
                yield Button(self._label(self._cancel_button, "Cancel"), id="cancel")

    def on_mount(self) -> None:
        """Focus directory widget on mount and set initial path."""
        dir_nav = self.query_one(DirectoryNavigation)
        current_path_label = self.query_one("#current_path_display", Label)
        current_path_label.update(str(dir_nav.location))
        
        # Initialize breadcrumbs
        self._update_breadcrumbs(dir_nav.location)

        dir_nav.focus()

    def _set_error(self, message: str = "") -> None:
        """Set or clear the error message.

        Args:
            message: Optional message to show as an error.
        """
        self.query_one(Dialog).border_subtitle = message

    @on(DriveNavigation.DriveSelected)
    def _change_drive(self, event: DriveNavigation.DriveSelected) -> None:
        """Reload DirectoryNavigation in response to drive change."""
        """Reload DirectoryNavigation in response to drive change."""
        dir_nav = self.query_one(DirectoryNavigation)
        dir_nav.location = event.drive_root

    @on(DirectoryNavigation.Changed)
    def _on_directory_changed(self, event: DirectoryNavigation.Changed) -> None:
        """Clear any error and update the path display."""
        self._set_error()
        current_path_label = self.query_one("#current_path_display", Label)
        current_path_label.update(str(event.control.location))
        
        # Update breadcrumbs
        self._update_breadcrumbs(event.control.location)


    @on(DirectoryNavigation.Changed)
    def _clear_error(self) -> None:
        """Clear any error that might be showing."""
        self._set_error()

    @on(DirectoryNavigation.PermissionError)
    def _show_permission_error(self) -> None:
        """Show any permission error bubbled up from the directory navigator."""
        self._set_error(self.ERROR_PERMISSION_ERROR)

    @on(Button.Pressed, "#cancel")
    def _cancel(self, event: Button.Pressed) -> None:
        """Cancel the dialog.

        Args:
            event: The even to handle.
        """
        event.stop()
        self.dismiss(None)

    def _action_hidden(self) -> None:
        """Action for toggling the display of hidden entries."""
        self.query_one(DirectoryNavigation).toggle_hidden()
        self.notify("Hidden files toggled", timeout=2)
    
    def action_focus_path_input(self) -> None:
        """Toggle and focus the path input field."""
        try:
            path_container = self.query_one("#path-input-container")
            path_input = self.query_one("#path-input", Input)
            
            # Toggle visibility
            if path_container.has_class("hidden"):
                path_container.remove_class("hidden")
                # Set current path as the initial value
                dir_nav = self.query_one(DirectoryNavigation)
                path_input.value = str(dir_nav.location)
                path_input.focus()
                # Select all text in the input
                path_input.selection = (0, len(path_input.value))
            else:
                path_container.add_class("hidden")
                # Return focus to directory navigation
                self.query_one(DirectoryNavigation).focus()
        except Exception as e:
            self.notify(f"Error toggling path input: {e}", severity="error", timeout=2)
    
    def action_refresh(self) -> None:
        """Refresh the current directory listing."""
        dir_nav = self.query_one(DirectoryNavigation)
        # Force refresh by resetting location
        current = dir_nav.location
        dir_nav.location = current
        self.notify("Directory refreshed", timeout=2)
    
    def action_bookmark_current(self) -> None:
        """Bookmark the current directory."""
        dir_nav = self.query_one(DirectoryNavigation)
        current_path = dir_nav.location
        # This would need to be implemented with proper bookmark storage
        self.notify(f"Bookmarked: {current_path.name}", timeout=2)
    
    def action_focus_search(self) -> None:
        """Toggle search mode and focus search input."""
        self.search_active = not self.search_active
        if self.search_active:
            try:
                search_input = self.query_one("#search-input", Input)
                search_input.focus()
            except Exception:
                pass
    
    def _update_breadcrumbs(self, path: Path) -> None:
        """Update breadcrumb navigation."""
        try:
            breadcrumb_container = self.query_one("#path-breadcrumbs", Horizontal)
            breadcrumb_container.remove_children()
            
            parts = path.parts
            for i, part in enumerate(parts):
                partial_path = Path(*parts[:i+1])
                
                # Create button for each path component
                btn = Button(part, variant="default", classes="breadcrumb-btn")
                btn.tooltip = str(partial_path)  # Store full path in tooltip
                breadcrumb_container.mount(btn)
                
                # Add separator if not last
                if i < len(parts) - 1:
                    breadcrumb_container.mount(Label("/", classes="breadcrumb-separator"))
        except Exception as e:
            # Silently fail if breadcrumbs can't be updated
            pass

    @on(Button.Pressed, ".breadcrumb-btn")
    def _on_breadcrumb_click(self, event: Button.Pressed) -> None:
        """Handle breadcrumb navigation clicks."""
        if event.button.tooltip:
            try:
                path = Path(event.button.tooltip)
                dir_nav = self.query_one(DirectoryNavigation)
                dir_nav.location = path
            except Exception:
                pass

    @on(Input.Changed, "#search-input")
    def _on_search_changed(self, event: Input.Changed) -> None:
        """Handle search input changes."""
        try:
            dir_nav = self.query_one(DirectoryNavigation)
            dir_nav.search_filter = event.value
        except Exception:
            pass
    
    @on(Button.Pressed, "#clear-search")
    def _on_clear_search(self) -> None:
        """Clear the search input."""
        try:
            search_input = self.query_one("#search-input", Input)
            search_input.value = ""
            self.search_active = False
        except Exception:
            pass

    def watch_search_active(self, active: bool) -> None:
        """React to search_active changes."""
        try:
            search_container = self.query_one("#search-container")
            search_container.set_class(active, "visible")
        except Exception:
            pass
    
    @on(Button.Pressed, "#go-to-path")
    @on(Input.Submitted, "#path-input")
    def _on_path_input_submit(self, event=None) -> None:
        """Handle path input submission."""
        try:
            path_input = self.query_one("#path-input", Input)
            path_str = path_input.value.strip()
            
            if not path_str:
                return
            
            # Expand user home directory if needed
            if path_str.startswith("~"):
                path = Path(path_str).expanduser()
            else:
                path = Path(path_str)
            
            # Make path absolute if it's relative
            if not path.is_absolute():
                dir_nav = self.query_one(DirectoryNavigation)
                path = dir_nav.location / path
            
            # Resolve the path
            path = path.resolve()
            
            # Check if path exists
            if not path.exists():
                self.notify(f"Path does not exist: {path}", severity="error", timeout=3)
                return
            
            # Navigate to the path
            dir_nav = self.query_one(DirectoryNavigation)
            if path.is_dir():
                dir_nav.location = path
            else:
                # If it's a file, navigate to its parent directory
                dir_nav.location = path.parent
                # TODO: Ideally, we would also select the file in the list
            
            # Hide the path input
            path_container = self.query_one("#path-input-container")
            path_container.add_class("hidden")
            dir_nav.focus()
            
        except Exception as e:
            self.notify(f"Error navigating to path: {e}", severity="error", timeout=3)
    
    @on(Button.Pressed, "#cancel-path-input")
    def _on_cancel_path_input(self) -> None:
        """Cancel path input and hide the container."""
        try:
            path_container = self.query_one("#path-input-container")
            path_container.add_class("hidden")
            self.query_one(DirectoryNavigation).focus()
        except Exception:
            pass


### base_dialog.py ends here
