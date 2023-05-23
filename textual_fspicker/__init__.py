"""A library that provides a widgets for selecting things from the filesystem."""

######################################################################
# Main app information.
__author__     = "Dave Pearson"
__copyright__  = "Copyright 2023, Dave Pearson"
__credits__    = [ "Dave Pearson" ]
__maintainer__ = "Dave Pearson"
__email__      = "davep@davep.org"
__version__    = "0.0.5"
__licence__    = "MIT"

##############################################################################
# Local imports.
from .file_open        import FileOpen
from .file_save        import FileSave
from .select_directory import SelectDirectory
from .path_filters     import Filters

##############################################################################
# Export the imports.
__all__ = [ "FileOpen", "FileSave", "SelectDirectory", "Filters" ]

### __init__.py ends here
