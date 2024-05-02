#!/usr/bin/python3
"""Defines the unittests for file: console.py"""
import unittest
import os
import inspect
import pep8
from io import StringIO
from unittest.mock import patch
from console import HBNBCommand
from models.engine.file_storage import FileStorage


class TestHBNBCommandConsole(unittest.TestCase):
    """Unittests for the HBNB command interpreter"""

    @classmethod
    def setUpClass(cls):
        """
        HBNBCommand testing setup
        
        Temporarily rename any existing file.json
        Reset FileStorage objects dictionary
        Create an instance of the command interpreter
        """
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass
        cls.HBNB = HBNBCommand()

    @classmethod
    def tearDownClass(cls):
        """
        HBNBCommand testing teardown
        
        Restore original file.json
        Delete the test HBNBCommand instance
        """
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass
        del cls.HBNB

    def setUp(self):
        """Reset FileStorage objects dict"""
        FileStorage._FileStorage__objects = {}

    def tearDown(self):
        """Delete any created file.json"""
        try:
            os.remove("file.json")
        except IOError:
            pass

    def test_create(self):
        """
        Tests for the create command of all components
        
        BaseModel/Users/State/City/Place/Amenities/Reviews
        """
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("create BaseModel")
            bm = f.getvalue().strip()

        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("create User")
            us = f.getvalue().strip()

        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("create State")
            st = f.getvalue().strip()

        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("create Place")
            pl = f.getvalue().strip()

        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("create City")
            ct = f.getvalue().strip()

        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("create Amenity")
            am = f.getvalue().strip()

        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("create Review")
            rv = f.getvalue().strip()

    def test_create_for_errors(self):
        """Test create command errors"""
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("create")
            self.assertEqual(
                "** class name missing **\n", f.getvalue())
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("create asdfsfsd")
            self.assertEqual(
                "** class doesn't exist **\n", f.getvalue())

    def test_HBNBCommand_class_docstring(self):
        """Test for the HBNBCommand class docstring"""
        self.assertIsNot(HBNBCommand.__doc__, None,
                         "HBNBCommand class needs a docstring")
        self.assertTrue(len(HBNBCommand.__doc__) >= 1,
                        "HBNBCommand class needs a docstring")
