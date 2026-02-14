# rzem-ai-secondbrain

A personal knowledge management system (second brain) for storing, organizing, and retrieving notes.

## Features

- 📝 Create and manage notes with titles, content, and tags
- 🔍 Search notes by title, content, or tags
- 🏷️ Organize notes with tags
- 💾 Persistent JSON-based storage
- 🖥️ Simple command-line interface
- 🐍 Pure Python implementation with no external dependencies

## Installation

No installation required! Just clone the repository and use Python 3.6 or higher.

```bash
git clone https://github.com/rzem-ai/rzem-ai-secondbrain.git
cd rzem-ai-secondbrain
```

## Usage

### Command-Line Interface

The second brain can be used directly from the command line:

```bash
python secondbrain.py <command> [args]
```

### Available Commands

#### Add a Note
```bash
python secondbrain.py add "My First Note" "This is the content of my note" python tutorial
```

#### List All Notes
```bash
python secondbrain.py list
```

#### Search Notes
```bash
python secondbrain.py search python
```

#### Get Notes by Tag
```bash
python secondbrain.py tag tutorial
```

#### List All Tags
```bash
python secondbrain.py tags
```

#### Get a Specific Note
```bash
python secondbrain.py get <note_id>
```

#### Delete a Note
```bash
python secondbrain.py delete <note_id>
```

### Python API

You can also use the second brain as a Python module:

```python
from secondbrain import SecondBrain

# Initialize the brain
brain = SecondBrain()

# Add a note
note = brain.add_note(
    title="Python Basics",
    content="Python is a high-level programming language",
    tags=["python", "programming", "tutorial"]
)

# Search for notes
results = brain.search_notes("python")

# Get notes by tag
python_notes = brain.get_notes_by_tag("python")

# List all notes
all_notes = brain.list_notes()

# Get all tags
tags = brain.get_all_tags()
```

## Examples

### Creating a Knowledge Base

```bash
# Add programming notes
python secondbrain.py add "Python Basics" "Variables, functions, and control flow" python basics tutorial

python secondbrain.py add "Python Advanced" "Decorators, generators, and metaclasses" python advanced

# Add project ideas
python secondbrain.py add "Project Ideas" "Build a CLI tool for managing tasks" projects ideas

# Search for Python-related notes
python secondbrain.py search python

# Get all notes tagged as tutorials
python secondbrain.py tag tutorial

# View all available tags
python secondbrain.py tags
```

## Data Storage

Notes are stored in a JSON file (`brain_data.json` by default) in the following format:

```json
{
  "notes": {
    "20260214123456789": {
      "id": "20260214123456789",
      "title": "My Note",
      "content": "Note content here",
      "tags": ["tag1", "tag2"],
      "created_at": "2026-02-14T12:34:56.789",
      "updated_at": "2026-02-14T12:34:56.789"
    }
  }
}
```

## Testing

Run the test suite to verify functionality:

```bash
python test_secondbrain.py
```

Or with verbose output:

```bash
python test_secondbrain.py -v
```

## Development

### Project Structure

```
rzem-ai-secondbrain/
├── secondbrain.py          # Main module with Note and SecondBrain classes
├── test_secondbrain.py     # Comprehensive test suite
├── README.md               # This file
├── LICENSE                 # MIT License
└── brain_data.json         # Data storage (created automatically)
```

### Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License - see LICENSE file for details.

## Future Enhancements

Potential features for future versions:
- Note linking (wiki-style links between notes)
- Markdown support for note content
- Export to various formats (PDF, HTML, Markdown)
- Web interface
- Encryption for sensitive notes
- Full-text search with ranking
- Note versioning and history