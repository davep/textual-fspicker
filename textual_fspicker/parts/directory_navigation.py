"""Provides a widget for directory navigation."""

##############################################################################
# Python imports.
from __future__  import annotations
from dataclasses import dataclass

##############################################################################
# Python imports.
from pathlib import Path

##############################################################################
# Textual imports.
from textual                     import work
from textual.reactive            import var
from textual.message             import Message
from textual.widgets             import OptionList
from textual.widgets.option_list import Option
from textual.worker              import get_current_worker

##############################################################################
class DirectoryEntry( Option ):
    """A directory entry for the `DirectoryNaviation` class."""

    def __init__( self, location: Path ) -> None:
        self.location: Path = location.resolve()
        """The location of this directory entry."""
        super().__init__( location.name )

##############################################################################
class DirectoryNavigation( OptionList ):
    """A directory navigation widget."""

    location: var[ Path ] = var[ Path ]( Path( "." ).resolve(), init=False )
    """The current location for the directory."""

    def __init__( self, location: Path | None = None ) -> None:
        """Initialise the directory navigation widget.

        Args:
            location: The starting location.
        """
        super().__init__()
        if location is not None:
            self.location = location

    def on_mount( self ) -> None:
        """Populate the widget once the DOM is ready."""
        self._load()

    def _settle_highlight( self ) -> None:
        """Settle the highlight somewhere useful if it's not anywhere."""
        if self.highlighted is None:
            self.highlighted = 0

    @property
    def is_root( self ) -> bool:
        """Are we at the root of the filesystem?"""
        # TODO: Worry about portability.
        return self.location == Path( self.location.root )

    @work(exclusive=True)
    def _load( self ) -> None:
        """Load the current directory data."""

        # Start out with a clear list.
        self.app.call_from_thread( self.clear_options )

        # If we're not at the root yet...
        if not self.is_root:
            # ...provide a path to the root.
            self.app.call_from_thread( self.add_option, DirectoryEntry( self.location / ".." ) )

        # Now loop over the directory, looking for directories within and
        # streaming them into the list via the app thread.
        worker = get_current_worker()
        for entry in self.location.iterdir():
            if entry.is_dir():
                # TODO: While this is a more pure way of doing things...
                # stream our way in one entry at a time, it can make it look
                # like there's a bit of flicker while loading. So perhaps,
                # in the end, decide to lost up the list and then blat them
                # into the OptionList in one go.
                self.app.call_from_thread(
                    self.add_option, DirectoryEntry( self.location / entry.name )
                )
            if worker.is_cancelled:
                return

        # Finally, ensure the first item is highlight.
        self.app.call_from_thread( self._settle_highlight )

    def _watch_location( self ) -> None:
        """Reload the content if the location changes."""
        self._load()

    @dataclass
    class Changed( Message ):
        """Message sent when the current directory has changed."""

        location: Path
        """The new location."""

    def _on_option_list_option_selected( self, event: OptionList.OptionSelected ) -> None:
        """Handle an entry in the list being selected.

        Args:
            event: The event to handle.
        """
        event.stop()
        assert isinstance( event.option, DirectoryEntry )
        self.location = event.option.location
        self.post_message( self.Changed( self.location ) )

### directory_navigation.py ends here
