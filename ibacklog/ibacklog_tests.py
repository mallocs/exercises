
import unittest
from ibacklog import IBacklog, Story, SQLLiteDatastore

TEST_SQLITE_DB_FILENAME = 'test_ibacklog.db'

class TestIBacklogFunctions(unittest.TestCase):

    def setUp(self):
        pass

    def test_Add(self):
        backlog = IBacklog(SQLLiteDatastore(TEST_SQLITE_DB_FILENAME))
        story1 = Story("1", 3, 1)
        backlog.Add(story1)
        print(len(backlog.getStories()))

    def test_Remove(self):
        pass

    def test_getSprint(self):
        pass

    def tearDown(self):
        pass

    def _loadSqlFile(self, filename):
        pass

if __name__ == '__main__':
    unittest.main()
