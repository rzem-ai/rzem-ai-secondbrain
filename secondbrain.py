#!/usr/bin/env python3
"""
Second Brain - A personal knowledge management system

This module provides functionality for storing, organizing, and retrieving
notes in a personal knowledge base.
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Optional


class Note:
    """Represents a single note in the second brain."""
    
    def __init__(self, title: str, content: str, tags: Optional[List[str]] = None, 
                 note_id: Optional[str] = None, created_at: Optional[str] = None):
        self.id = note_id or self._generate_id()
        self.title = title
        self.content = content
        self.tags = tags or []
        self.created_at = created_at or datetime.now().isoformat()
        self.updated_at = datetime.now().isoformat()
    
    def _generate_id(self) -> str:
        """Generate a unique ID for the note."""
        return datetime.now().strftime("%Y%m%d%H%M%S%f")
    
    def to_dict(self) -> Dict:
        """Convert note to dictionary for serialization."""
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'tags': self.tags,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Note':
        """Create a Note from a dictionary."""
        return cls(
            title=data['title'],
            content=data['content'],
            tags=data.get('tags', []),
            note_id=data.get('id'),
            created_at=data.get('created_at')
        )
    
    def __str__(self) -> str:
        tags_str = f" [{', '.join(self.tags)}]" if self.tags else ""
        return f"Note: {self.title}{tags_str}\n{self.content}"


class SecondBrain:
    """Main class for managing the second brain knowledge base."""
    
    def __init__(self, storage_path: str = "brain_data.json"):
        self.storage_path = storage_path
        self.notes: Dict[str, Note] = {}
        self.load()
    
    def load(self):
        """Load notes from storage."""
        if os.path.exists(self.storage_path):
            try:
                with open(self.storage_path, 'r') as f:
                    data = json.load(f)
                    self.notes = {
                        note_id: Note.from_dict(note_data)
                        for note_id, note_data in data.get('notes', {}).items()
                    }
            except (json.JSONDecodeError, IOError) as e:
                print(f"Warning: Could not load brain data: {e}")
                self.notes = {}
    
    def save(self):
        """Save notes to storage."""
        data = {
            'notes': {
                note_id: note.to_dict()
                for note_id, note in self.notes.items()
            }
        }
        with open(self.storage_path, 'w') as f:
            json.dump(data, f, indent=2)
    
    def add_note(self, title: str, content: str, tags: Optional[List[str]] = None) -> Note:
        """Add a new note to the second brain."""
        note = Note(title, content, tags)
        self.notes[note.id] = note
        self.save()
        return note
    
    def get_note(self, note_id: str) -> Optional[Note]:
        """Retrieve a note by ID."""
        return self.notes.get(note_id)
    
    def update_note(self, note_id: str, title: Optional[str] = None, 
                   content: Optional[str] = None, tags: Optional[List[str]] = None) -> Optional[Note]:
        """Update an existing note."""
        note = self.notes.get(note_id)
        if not note:
            return None
        
        if title is not None:
            note.title = title
        if content is not None:
            note.content = content
        if tags is not None:
            note.tags = tags
        
        note.updated_at = datetime.now().isoformat()
        self.save()
        return note
    
    def delete_note(self, note_id: str) -> bool:
        """Delete a note by ID."""
        if note_id in self.notes:
            del self.notes[note_id]
            self.save()
            return True
        return False
    
    def list_notes(self) -> List[Note]:
        """List all notes."""
        return sorted(self.notes.values(), key=lambda n: n.created_at, reverse=True)
    
    def search_notes(self, query: str) -> List[Note]:
        """Search notes by title, content, or tags."""
        query = query.lower()
        results = []
        for note in self.notes.values():
            if (query in note.title.lower() or 
                query in note.content.lower() or 
                any(query in tag.lower() for tag in note.tags)):
                results.append(note)
        return sorted(results, key=lambda n: n.created_at, reverse=True)
    
    def get_notes_by_tag(self, tag: str) -> List[Note]:
        """Get all notes with a specific tag."""
        tag = tag.lower()
        results = [note for note in self.notes.values() if tag in [t.lower() for t in note.tags]]
        return sorted(results, key=lambda n: n.created_at, reverse=True)
    
    def get_all_tags(self) -> List[str]:
        """Get all unique tags used in the brain."""
        tags = set()
        for note in self.notes.values():
            tags.update(note.tags)
        return sorted(tags)


def main():
    """Simple CLI interface for the second brain."""
    import sys
    
    brain = SecondBrain()
    
    if len(sys.argv) < 2:
        print("Usage: python secondbrain.py <command> [args]")
        print("\nCommands:")
        print("  add <title> <content> [tags...]    - Add a new note")
        print("  list                                - List all notes")
        print("  search <query>                      - Search notes")
        print("  tag <tag>                           - Find notes by tag")
        print("  tags                                - List all tags")
        print("  get <note_id>                       - Get a specific note")
        print("  delete <note_id>                    - Delete a note")
        return
    
    command = sys.argv[1].lower()
    
    if command == "add":
        if len(sys.argv) < 4:
            print("Error: add requires title and content")
            return
        title = sys.argv[2]
        content = sys.argv[3]
        tags = sys.argv[4:] if len(sys.argv) > 4 else []
        note = brain.add_note(title, content, tags)
        print(f"Added note with ID: {note.id}")
        print(note)
    
    elif command == "list":
        notes = brain.list_notes()
        if not notes:
            print("No notes found.")
        else:
            print(f"Found {len(notes)} note(s):\n")
            for note in notes:
                print(f"ID: {note.id}")
                print(f"Title: {note.title}")
                if note.tags:
                    print(f"Tags: {', '.join(note.tags)}")
                print(f"Created: {note.created_at}")
                print(f"Preview: {note.content[:100]}...")
                print("-" * 50)
    
    elif command == "search":
        if len(sys.argv) < 3:
            print("Error: search requires a query")
            return
        query = sys.argv[2]
        notes = brain.search_notes(query)
        if not notes:
            print(f"No notes found matching '{query}'.")
        else:
            print(f"Found {len(notes)} note(s) matching '{query}':\n")
            for note in notes:
                print(f"ID: {note.id}")
                print(f"Title: {note.title}")
                if note.tags:
                    print(f"Tags: {', '.join(note.tags)}")
                print("-" * 50)
    
    elif command == "tag":
        if len(sys.argv) < 3:
            print("Error: tag requires a tag name")
            return
        tag = sys.argv[2]
        notes = brain.get_notes_by_tag(tag)
        if not notes:
            print(f"No notes found with tag '{tag}'.")
        else:
            print(f"Found {len(notes)} note(s) with tag '{tag}':\n")
            for note in notes:
                print(f"ID: {note.id}")
                print(f"Title: {note.title}")
                print("-" * 50)
    
    elif command == "tags":
        tags = brain.get_all_tags()
        if not tags:
            print("No tags found.")
        else:
            print(f"All tags ({len(tags)}):")
            for tag in tags:
                print(f"  - {tag}")
    
    elif command == "get":
        if len(sys.argv) < 3:
            print("Error: get requires a note ID")
            return
        note_id = sys.argv[2]
        note = brain.get_note(note_id)
        if note:
            print(note)
            print(f"\nID: {note.id}")
            print(f"Created: {note.created_at}")
            print(f"Updated: {note.updated_at}")
        else:
            print(f"Note with ID '{note_id}' not found.")
    
    elif command == "delete":
        if len(sys.argv) < 3:
            print("Error: delete requires a note ID")
            return
        note_id = sys.argv[2]
        if brain.delete_note(note_id):
            print(f"Deleted note with ID: {note_id}")
        else:
            print(f"Note with ID '{note_id}' not found.")
    
    else:
        print(f"Unknown command: {command}")


if __name__ == "__main__":
    main()
