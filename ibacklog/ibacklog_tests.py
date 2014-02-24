
import unittest
import sqlite3
import os
from ibacklog import IBacklog, Story, SQLLiteDatastore, StoryNotFoundError, IDatastore
from unittest.mock import Mock

TEST_SQLITE_DB_FILENAME = '_test_ibacklog.db'
TEST_DB1_FILENAME = 'test1.sql'
class TestIBacklogFunctions(unittest.TestCase):

    def setUp(self):
        if os.path.isfile(TEST_SQLITE_DB_FILENAME):
            raise RuntimeError("Could not create a new " + TEST_SQLITE_DB_FILENAME + ". File already exists.")
        self.backlog = IBacklog(SQLLiteDatastore(TEST_SQLITE_DB_FILENAME))
        
    def test_Add(self):

        story1 = Story("1", 3, 1)
        datastore_mock = Mock()
        datastore_mock.__class__ = IDatastore
        datastore_mock.createStory(story1)
        datastore_mock.createStory.assert_called_once_with(story1)
        backlog = IBacklog(datastore_mock)

        # make sure one Story is added to the datastore when the datastore is empty.

        countBeforeAdd = len(self.backlog.datastore.readStory())
        self.backlog.Add(story1)
        self.assertEqual(countBeforeAdd+1, len(self.backlog.datastore.readStory()))

        # make sure one Story is added to the datastore when the datastore is not empty.
        story2 = Story("2", 6, 2)
        self.backlog.Add(story2)
        self.assertEqual(countBeforeAdd+2, len(self.backlog.datastore.readStory()))

    def test_Remove(self):
        # make sure one story is removed if it is in the datastore.
        # make sure the story is returned.
        
        self._setStoryTableStateWithSQLFile(TEST_DB1_FILENAME)
        story1 = Story("1", 3, 1)
        datastore_mock = Mock()
        datastore_mock.__class__ = IDatastore
        datastore_mock.removeStory.return_value = story1
        datastore_mock.removeStory("1")
        datastore_mock.removeStory.assert_called_once_with("1")


        self._setStoryTableStateWithSQLFile(TEST_DB1_FILENAME)
        countBeforeRemove = len(self.backlog.datastore.readStory())
        story = self.backlog.Remove("1")
        self.assertEqual(countBeforeRemove-1, len(self.backlog.datastore.readStory()))
        
        # make sure an error is raised if it is not in the datastore.
        self.assertRaises(StoryNotFoundError, self.backlog.Remove, "1")

    def test_getSprint(self):
        self._setStoryTableStateWithSQLFile(TEST_DB1_FILENAME)

    def tearDown(self):
        os.remove(TEST_SQLITE_DB_FILENAME)

    def _setStoryTableStateWithSQLFile(self, filename):
        # Sets the state of the Story table with an sql script file.
        try:
            f = open(filename, 'r')
        except (IOError, e):
            print("Couldn't open " + filename)
        conn = sqlite3.connect(TEST_SQLITE_DB_FILENAME)
        with conn:
            cur = conn.cursor()
            cur.execute('''DROP TABLE IF EXISTS Stories''')
            cur.executescript(f.read())
            conn.commit()
            f.close()

if __name__ == '__main__':
    unittest.main()




