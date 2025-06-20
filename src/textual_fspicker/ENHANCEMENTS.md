# File Picker Enhancements

This document describes the enhancements made to the textual-fspicker module to improve user experience and functionality.

## New Features

### 1. Enhanced Keyboard Shortcuts
- **Ctrl+H** - Toggle hidden files (in addition to existing '.')
- **Ctrl+L** - Focus path input field for direct path entry
- **Ctrl+R** - Toggle recent locations panel
- **Ctrl+F** - Toggle search mode and focus search input
- **F5** - Refresh current directory
- **Ctrl+D** - Bookmark current directory (placeholder for future implementation)

### 2. Recent Locations Panel
- Shows recently accessed files and directories
- Toggle visibility with Ctrl+R
- Click to quickly navigate to recent locations
- Placeholder for persistent storage (needs implementation)

### 3. Breadcrumb Navigation
- Visual path display with clickable components
- Click any path segment to navigate directly
- Better understanding of current location in filesystem hierarchy

### 4. Search Within Directory
- Real-time search filtering of directory contents
- Toggle with Ctrl+F
- Filters files and folders by name
- Clear button to reset search

### 5. Improved Visual Feedback
- Notifications for keyboard actions
- Better error messages
- Search active indicator

## Implementation Details

### Modified Files

1. **base_dialog.py**
   - Added new keyboard bindings
   - Added reactive properties for UI state
   - Implemented breadcrumb navigation
   - Added recent locations panel
   - Added search container
   - Implemented all keyboard action handlers

2. **parts/directory_navigation.py**
   - Added `search_filter` reactive variable
   - Modified `hide()` method to respect search filter
   - Added `_watch_search_filter()` method
   - Modified `_repopulate_display()` to handle search state

### Code Structure

The enhancements maintain backward compatibility while adding new optional features. The UI components are hidden by default and can be toggled via keyboard shortcuts.

### CSS Additions

New CSS rules were added for:
- Breadcrumb navigation styling
- Recent locations panel
- Search container
- Visibility toggles

## Usage Example

```python
from textual_fspicker import FileOpen

# Use the enhanced file picker
file_dialog = FileOpen(
    title="Select a file",
    filters=Filters(
        ("Python Files", "*.py"),
        ("All Files", "*.*")
    )
)

# All new features are available via keyboard shortcuts
```

## Future Improvements

1. **Persistent Storage for Recent Locations**
   - Save to user config directory
   - Load on startup
   - Configurable max items

2. **Bookmarks System**
   - Save frequently used directories
   - Manage bookmarks UI
   - Persistent storage

3. **Advanced Search**
   - Regex support
   - Case sensitivity toggle
   - Search in subdirectories option

4. **File Preview**
   - Preview pane for text files
   - Image thumbnails
   - File metadata display

## Testing

The enhancements have been tested with:
- Various directory structures
- Hidden files toggle
- Search functionality
- Breadcrumb navigation
- Keyboard shortcuts

## Contributing Upstream

These enhancements are designed to be contributed back to the original textual-fspicker project. They:
- Maintain backward compatibility
- Follow the existing code style
- Add optional features that don't change default behavior
- Include proper documentation

To contribute:
1. Fork the original repository
2. Apply these changes
3. Add tests for new features
4. Submit a pull request with this documentation