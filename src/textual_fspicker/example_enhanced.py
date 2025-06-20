#!/usr/bin/env python3
"""Example demonstrating the enhanced file picker with new features."""

from pathlib import Path
from textual.app import App, ComposeResult
from textual.widgets import Button, Label, Footer, Header
from textual.containers import Container, Vertical

from file_open import FileOpen
from file_save import FileSave
from path_filters import Filters


class EnhancedFilePickerExample(App):
    """Example app demonstrating enhanced file picker features."""
    
    CSS = """
    Container {
        align: center middle;
        padding: 2;
    }
    
    #result {
        margin-top: 2;
        padding: 1;
        border: solid $primary;
        height: 3;
    }
    
    Button {
        margin: 1;
    }
    """
    
    def compose(self) -> ComposeResult:
        yield Header()
        with Container():
            with Vertical():
                yield Label("Enhanced File Picker Demo", id="title")
                yield Label("New Features:", id="features")
                yield Label("• Ctrl+H - Toggle hidden files")
                yield Label("• Ctrl+L - Focus path input")
                yield Label("• Ctrl+R - Show recent locations")
                yield Label("• Ctrl+F - Search in directory")
                yield Label("• F5 - Refresh directory")
                yield Label("• Breadcrumb navigation")
                yield Button("Open File", id="open")
                yield Button("Save File", id="save")
                yield Label("No file selected", id="result")
        yield Footer()
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses."""
        if event.button.id == "open":
            self.push_screen(
                FileOpen(
                    title="Open File - Try the new features!",
                    filters=Filters(
                        ("Python Files", "*.py"),
                        ("Text Files", "*.txt"),
                        ("All Files", "*.*")
                    )
                ),
                self.handle_file_selected
            )
        elif event.button.id == "save":
            self.push_screen(
                FileSave(
                    title="Save File - Try the new features!",
                    filters=Filters(
                        ("Python Files", "*.py"),
                        ("Text Files", "*.txt"),
                        ("All Files", "*.*")
                    ),
                    default_filename="example.txt"
                ),
                self.handle_file_selected
            )
    
    def handle_file_selected(self, path: Path | None) -> None:
        """Handle file selection."""
        result = self.query_one("#result", Label)
        if path:
            result.update(f"Selected: {path}")
        else:
            result.update("No file selected")


if __name__ == "__main__":
    app = EnhancedFilePickerExample()
    app.run()