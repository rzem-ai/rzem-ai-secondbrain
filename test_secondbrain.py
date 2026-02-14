#!/usr/bin/env python3
"""
Test suite for the Second Brain module
"""

import unittest
import os
import json
from secondbrain import Note, SecondBrain


class TestNote(unittest.TestCase):
    """Test the Note class."""
    
    def test_note_creation(self):
        """Test creating a note."""
        note = Note("Test Title", "Test content", ["tag1", "tag2"])
        self.assertEqual(note.title, "Test Title")
        self.assertEqual(note.content, "Test content")
        self.assertEqual(note.tags, ["tag1", "tag2"])
        self.assertIsNotNone(note.id)
        self.assertIsNotNone(note.created_at)
    
    def test_note_without_tags(self):
        """Test creating a note without tags."""
        note = Note("Title", "Content")
        self.assertEqual(note.tags, [])
    
    def test_note_to_dict(self):
        """Test converting note to dictionary."""
        note = Note("Title", "Content", ["tag1"])
        data = note.to_dict()
        self.assertEqual(data['title'], "Title")
        self.assertEqual(data['content'], "Content")
        self.assertEqual(data['tags'], ["tag1"])
        self.assertIn('id', data)
        self.assertIn('created_at', data)
        self.assertIn('updated_at', data)
    
    def test_note_from_dict(self):
        """Test creating note from dictionary."""
        data = {
            'id': '123',
            'title': 'Test',
            'content': 'Test content',
            'tags': ['tag1'],
            'created_at': '2026-01-01T00:00:00'
        }
        note = Note.from_dict(data)
        self.assertEqual(note.id, '123')
        self.assertEqual(note.title, 'Test')
        self.assertEqual(note.content, 'Test content')
        self.assertEqual(note.tags, ['tag1'])
    
    def test_note_string_representation(self):
        """Test note string representation."""
        note = Note("Title", "Content", ["tag1"])
        str_repr = str(note)
        self.assertIn("Title", str_repr)
        self.assertIn("Content", str_repr)
        self.assertIn("tag1", str_repr)


class TestSecondBrain(unittest.TestCase):
    """Test the SecondBrain class."""
    
    def setUp(self):
        """Set up test environment."""
        self.test_storage = "test_brain_data.json"
        if os.path.exists(self.test_storage):
            os.remove(self.test_storage)
        self.brain = SecondBrain(self.test_storage)
    
    def tearDown(self):
        """Clean up test environment."""
        if os.path.exists(self.test_storage):
            os.remove(self.test_storage)
    
    def test_add_note(self):
        """Test adding a note."""
        note = self.brain.add_note("Test Title", "Test content", ["tag1"])
        self.assertIsNotNone(note.id)
        self.assertEqual(note.title, "Test Title")
        self.assertEqual(note.content, "Test content")
        self.assertEqual(note.tags, ["tag1"])
        self.assertEqual(len(self.brain.notes), 1)
    
    def test_get_note(self):
        """Test retrieving a note."""
        note = self.brain.add_note("Title", "Content")
        retrieved = self.brain.get_note(note.id)
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.title, "Title")
        self.assertEqual(retrieved.content, "Content")
    
    def test_get_nonexistent_note(self):
        """Test retrieving a nonexistent note."""
        result = self.brain.get_note("nonexistent")
        self.assertIsNone(result)
    
    def test_update_note(self):
        """Test updating a note."""
        note = self.brain.add_note("Original", "Original content")
        updated = self.brain.update_note(note.id, title="Updated", content="Updated content")
        self.assertIsNotNone(updated)
        self.assertEqual(updated.title, "Updated")
        self.assertEqual(updated.content, "Updated content")
    
    def test_update_note_partial(self):
        """Test partially updating a note."""
        note = self.brain.add_note("Title", "Content", ["tag1"])
        updated = self.brain.update_note(note.id, title="New Title")
        self.assertEqual(updated.title, "New Title")
        self.assertEqual(updated.content, "Content")
        self.assertEqual(updated.tags, ["tag1"])
    
    def test_delete_note(self):
        """Test deleting a note."""
        note = self.brain.add_note("Title", "Content")
        result = self.brain.delete_note(note.id)
        self.assertTrue(result)
        self.assertEqual(len(self.brain.notes), 0)
    
    def test_delete_nonexistent_note(self):
        """Test deleting a nonexistent note."""
        result = self.brain.delete_note("nonexistent")
        self.assertFalse(result)
    
    def test_list_notes(self):
        """Test listing notes."""
        self.brain.add_note("Note 1", "Content 1")
        self.brain.add_note("Note 2", "Content 2")
        self.brain.add_note("Note 3", "Content 3")
        notes = self.brain.list_notes()
        self.assertEqual(len(notes), 3)
    
    def test_search_notes_by_title(self):
        """Test searching notes by title."""
        self.brain.add_note("Python Tutorial", "Learn Python")
        self.brain.add_note("Java Tutorial", "Learn Java")
        self.brain.add_note("Python Advanced", "Advanced Python")
        results = self.brain.search_notes("Python")
        self.assertEqual(len(results), 2)
    
    def test_search_notes_by_content(self):
        """Test searching notes by content."""
        self.brain.add_note("Tutorial", "Learn Python programming")
        self.brain.add_note("Guide", "Learn Java programming")
        results = self.brain.search_notes("Python")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].title, "Tutorial")
    
    def test_search_notes_by_tag(self):
        """Test searching notes by tag."""
        self.brain.add_note("Note 1", "Content", ["python", "tutorial"])
        self.brain.add_note("Note 2", "Content", ["java"])
        results = self.brain.search_notes("python")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].title, "Note 1")
    
    def test_search_case_insensitive(self):
        """Test that search is case-insensitive."""
        self.brain.add_note("Python", "Content")
        results = self.brain.search_notes("python")
        self.assertEqual(len(results), 1)
        results = self.brain.search_notes("PYTHON")
        self.assertEqual(len(results), 1)
    
    def test_get_notes_by_tag(self):
        """Test getting notes by tag."""
        self.brain.add_note("Note 1", "Content", ["python", "tutorial"])
        self.brain.add_note("Note 2", "Content", ["python", "advanced"])
        self.brain.add_note("Note 3", "Content", ["java"])
        results = self.brain.get_notes_by_tag("python")
        self.assertEqual(len(results), 2)
    
    def test_get_notes_by_tag_case_insensitive(self):
        """Test that tag search is case-insensitive."""
        self.brain.add_note("Note", "Content", ["Python"])
        results = self.brain.get_notes_by_tag("python")
        self.assertEqual(len(results), 1)
    
    def test_get_all_tags(self):
        """Test getting all unique tags."""
        self.brain.add_note("Note 1", "Content", ["python", "tutorial"])
        self.brain.add_note("Note 2", "Content", ["python", "advanced"])
        self.brain.add_note("Note 3", "Content", ["java"])
        tags = self.brain.get_all_tags()
        self.assertEqual(set(tags), {"python", "tutorial", "advanced", "java"})
    
    def test_save_and_load(self):
        """Test saving and loading brain data."""
        self.brain.add_note("Title 1", "Content 1", ["tag1"])
        self.brain.add_note("Title 2", "Content 2", ["tag2"])
        
        # Create a new brain instance to test loading
        new_brain = SecondBrain(self.test_storage)
        self.assertEqual(len(new_brain.notes), 2)
        
        # Verify content
        notes = new_brain.list_notes()
        titles = [n.title for n in notes]
        self.assertIn("Title 1", titles)
        self.assertIn("Title 2", titles)
    
    def test_persistence(self):
        """Test that data persists across instances."""
        note = self.brain.add_note("Persistent", "This should persist")
        note_id = note.id
        
        # Create new brain instance
        new_brain = SecondBrain(self.test_storage)
        retrieved = new_brain.get_note(note_id)
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.title, "Persistent")
    
    def test_empty_brain(self):
        """Test operations on empty brain."""
        self.assertEqual(len(self.brain.list_notes()), 0)
        self.assertEqual(len(self.brain.search_notes("test")), 0)
        self.assertEqual(len(self.brain.get_all_tags()), 0)
    
    def test_storage_file_created(self):
        """Test that storage file is created after adding a note."""
        self.assertFalse(os.path.exists(self.test_storage))
        self.brain.add_note("Title", "Content")
        self.assertTrue(os.path.exists(self.test_storage))


if __name__ == '__main__':
    unittest.main()
