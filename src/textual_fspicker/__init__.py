"""A library that provides widgets for selecting things from the filesystem."""

##############################################################################
# Python imports.
from importlib.metadata import version

######################################################################
# Main app information.
__author__ = "Dave Pearson"
__copyright__ = "Copyright 2023, Dave Pearson"
__credits__ = ["Dave Pearson"]
__maintainer__ = "Dave Pearson"
__email__ = "davep@davep.org"
__version__ = version("textual_fspicker")
__licence__ = "MIT"

##############################################################################
# Local imports.
from .file_open import FileOpen
from .file_save import FileSave
from .icons import Icons
from .path_filters import Filters
from .path_maker import MakePath
from .select_directory import SelectDirectory

##############################################################################
# Export the imports.
__all__ = ["FileOpen", "FileSave", "Icons", "SelectDirectory", "Filters", "MakePath"]

### __init__.py ends here
