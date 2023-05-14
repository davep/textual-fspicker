"""Provides a widget for directory navigation."""

##############################################################################
# Python imports.
from __future__        import annotations
from dataclasses       import dataclass
from datetime          import datetime
from pathlib           import Path
from typing            import Iterable
from typing_extensions import Final

##############################################################################
# Rich imports.
from rich.console import RenderableType
from rich.table   import Table
from rich.text    import Text

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

    FOLDER_ICON: Final[ RenderableType ] = Text.from_markup( ":file_folder:" )
    """The icon to use for a folder."""

    FILE_ICON: Final[ RenderableType ] = Text.from_markup( ":page_facing_up:" )
    """The icon to use for a file."""

    def __init__( self, location: Path ) -> None:
        self.location: Path = location.absolute()
        """The location of this directory entry."""
        super().__init__( self._as_renderable( location ) )

    @staticmethod
    def _mtime( location: Path ) -> str:
        """Get a formatted modification time for the given location.

        Args:
            location: The location to get the modification time for.

        Returns:
            The formatted modification time, to the nearest second.
        """
        try:
            mtime = location.stat().st_mtime
        except FileNotFoundError:
            mtime = 0
        return datetime.fromtimestamp( int( mtime ) ).isoformat().replace( "T", " " )

    @staticmethod
    def _size( location: Path ) -> str:
        """Get a formatted size for the given location.

        Args:
            location: The location to get the size for.

        Returns:
            The formatted size.
        """
        try:
            entry_size = location.stat().st_size
        except FileNotFoundError:
            entry_size = 0
        # TODO: format well for a file browser.
        return str( entry_size )

    def _dir( self, prompt: Table, location: Path ) -> RenderableType:
        prompt.add_column( no_wrap=True, width=1 )
        prompt.add_column( no_wrap=True, justify="left", width=3 )
        prompt.add_column( no_wrap=True, justify="left", ratio=1 )
        prompt.add_column( no_wrap=True, justify="right", width=10 )
        prompt.add_column( no_wrap=True, justify="right", width=20 )
        prompt.add_column( no_wrap=True, width=1 )
        prompt.add_row(
            "",
            self.FOLDER_ICON,
            location.name,
            self._size( location ),
            self._mtime( location ),
            ""
        )
        return prompt

    def _file( self, prompt: Table, location: Path ) -> RenderableType:
        prompt.add_column( no_wrap=True, width=1 )
        prompt.add_column( no_wrap=True, justify="left", width=3 )
        prompt.add_column( no_wrap=True, justify="left", ratio=1 )
        prompt.add_column( no_wrap=True, justify="right", width=10 )
        prompt.add_column( no_wrap=True, justify="right", width=20 )
        prompt.add_column( no_wrap=True, width=1 )
        prompt.add_row(
            "",
            self.FILE_ICON,
            location.name,
            self._size( location ),
            self._mtime( location ),
            ""
        )
        return prompt

    def _as_renderable( self, location: Path ) -> RenderableType:
        """Create the renderable for this entry.

        Args:
            location: The location to turn into a renderable.

        Returns:
            The entry as a Rich renderable.
        """
        return ( { True: self._dir, False: self._file }[ location.is_dir() ] )( Table.grid( expand=True ), location )

##############################################################################
class DirectoryNavigation( OptionList ):
    """A directory navigation widget.

    Provides a single-pane widget that lets the user navigate their way
    through a filesystenm, changing in and out of directories, and selecting
    a file.
    """

    @dataclass
    class _BaseMessage( Message ):
        """Base class for directory navigation messages."""

        control: DirectoryNavigation
        """The directory navigation control sending the message."""

    class Changed( _BaseMessage ):
        """Message sent when the current directory has changed."""

    @dataclass
    class _PathMessage( _BaseMessage ):
        """Base class for messages relating to a location in the filesystem."""

        path: Path = Path()
        """The path to the entry that was selected."""

    class Highlighted( _PathMessage ):
        """Message sent when an entry in the display is highlighted."""

    class Selected( _PathMessage ):
        """Message sent when an entry in the filesystem is selected."""

    _location: var[ Path ] = var[ Path ]( Path( "." ).absolute(), init=False )
    """The current location for the directory."""

    show_files: var[ bool ] = var( True )
    """Should files be shown and be selectable?"""

    show_hidden: var[ bool ] = var( False )
    """Should hidden entries be shown?"""

    sort_display: var[ bool ] = var( True )
    """Should the display be sorted?"""

    def __init__( self, location: Path | str | None = None ) -> None:
        """Initialise the directory navigation widget.

        Args:
            location: The starting location.
        """
        super().__init__()
        self._mounted                       = False
        self.location                       = Path( "~" if location is None else location ).expanduser().absolute()
        self._entries: list[DirectoryEntry] = []

    @property
    def location( self ) -> Path:
        """The current location of the navigation widget."""
        return self._location

    @location.setter
    def location( self, new_location: Path | str ) -> None:
        new_location = Path( new_location ).expanduser().absolute()
        if self._mounted:
            self._location = new_location
        else:
            self._initial_location = new_location

    def on_mount( self ) -> None:
        """Populate the widget once the DOM is ready."""
        self._mounted = True
        self._location = self._initial_location

    def _settle_highlight( self ) -> None:
        """Settle the highlight somewhere useful if it's not anywhere."""
        if self.highlighted is None:
            self.highlighted = 0

    @property
    def is_root( self ) -> bool:
        """Are we at the root of the filesystem?"""
        # TODO: Worry about portability.
        return self._location == Path( self._location.root )

    @staticmethod
    def is_hidden( path: Path ) -> bool:
        """Does the given path appear to be hidden?

        Args:
            path: The path to test.

        Returns:
            `True` if the path appears to be hidden, `False` if not.

        Note:
            For the moment this simply checks for the 'dot hack'. Eventually
            I'll extend this to detect hidden files in the most appropriate
            way for the current operating system.
        """
        return path.name.startswith( "." )

    def hide( self, path: Path ) -> bool:
        """Should we hide the given path?

        Args:
            path: The path to test.

        Returns:
            `True` if the path should be hidden, `False` if not.
        """
        return self.is_hidden( path ) and not self.show_hidden

    def _sort( self, entries: Iterable[ DirectoryEntry ] ) -> Iterable[ DirectoryEntry ]:
        """Sort the entries as per the value of `sort_display`."""
        if self.sort_display:
            return sorted( entries, key=lambda entry: ( not entry.location.is_dir(), entry.location.name ) )
        return entries

    def _repopulate_display( self ) -> None:
        """Repopulate the display of directories."""
        with self.app.batch_update():
            self.clear_options()
            if not self.is_root:
                self.add_option( DirectoryEntry( self._location / ".." ) )
            self.add_options( self._sort( entry for entry in self._entries if not self.hide( entry.location ) ) )
        self._settle_highlight()

    @work(exclusive=True)
    def _load( self ) -> None:
        """Load the current directory data."""

        # Because we might end up slicing and dicing the list, and there's
        # little point in reloading the data from the filesystem again if
        # all the user is doing is requesting hidden files be shown/hidden,
        # or the sort order be changed, or something, we're going to keep a
        # parallel copy of *all* possible options for the list and then
        # populate from that.
        self._entries = []

        # Now loop over the directory, looking for directories within and
        # streaming them into the list via the app thread.
        worker = get_current_worker()
        for entry in self._location.iterdir():
            if entry.is_dir() or ( entry.is_file and self.show_files ):
                self._entries.append( DirectoryEntry( self._location / entry.name ) )
            if worker.is_cancelled:
                return

        # Now that we've loaded everything up, let's make the call to update
        # the display.
        self.app.call_from_thread( self._repopulate_display )

    def _watch__location( self ) -> None:
        """Reload the content if the location changes."""
        self.post_message( self.Changed( self ) )
        self._load()

    def _watch_show_hidden( self ) -> None:
        """Refresh the display if the show-hidden flag has changed."""
        self._repopulate_display()

    def _watch_show_files( self ) -> None:
        """Reload the content if the show-files flag has changed."""
        self._load()

    def _watch_sort_display( self ) -> None:
        """Refresh the display if the sort option has been changed."""
        self._repopulate_display()

    def toggle_hidden( self ) -> None:
        """Toggle the display of hidden filesystem entries."""
        self.show_hidden = not self.show_hidden

    def _on_option_list_option_highlighted( self, event: OptionList.OptionHighlighted ) -> None:
        """Handle an entry in the list being highlighted.

        Args:
            event: The event to handle.
        """
        event.stop()
        if event.option is not None:
            assert isinstance( event.option, DirectoryEntry )
            self.post_message( self.Highlighted( self, event.option.location ) )

    def _on_option_list_option_selected( self, event: OptionList.OptionSelected ) -> None:
        """Handle an entry in the list being selected.

        Args:
            event: The event to handle.
        """
        event.stop()
        assert isinstance( event.option, DirectoryEntry )
        # If the use has selected a directory...
        if event.option.location.is_dir():
            # ...we do navigation and don't post anything from here.
            self._location = event.option.location.resolve()
        else:
            # If it's not a directory it should be a file; that should be a
            # selection event.
            self.post_message( self.Selected( self, event.option.location ) )

### directory_navigation.py ends here
