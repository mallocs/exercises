
import unittest
import sqlite3
import os
from ibacklog import IBacklog, Story, SQLLiteDatastore, StoryNotFoundError, IDatastore
from unittest.mock import Mock

class TestIBacklogFunctions(unittest.TestCase):

    def test_Add(self):
        # Make sure datastore.createStory is called once when IBacklog.Add is called.
        story1 = Story("1", 3, 1)
        datastore_mock = Mock()
        datastore_mock.__class__ = IDatastore
        datastore_mock.createStory(story1)
        datastore_mock.createStory.assert_called_once_with(story1)
        backlog = IBacklog(datastore_mock)
        backlog.Add(story1)

    def test_Remove(self):
        # Make sure datastore.deleteStory is called once when IBacklog.Remove is called.
        # Make sure the story is returned.
        
        story1 = Story("1", 3, 1)
        datastore_mock = Mock()
        datastore_mock.__class__ = IDatastore
        datastore_mock.deleteStory.return_value = story1
        datastore_mock.deleteStory("1")
        datastore_mock.deleteStory.assert_called_once_with("1")
        backlog = IBacklog(datastore_mock)
        actual_story = backlog.Remove("1")
        self.assertEqual(actual_story, story1)

    def test_RemoveRaisesException(self):
        # Make sure an exception is raised IBacklog.Remove is called with the Id of a story
        # that is not in the datastore.
        datastore_mock = Mock()
        datastore_mock.__class__ = IDatastore
        datastore_mock.deleteStory.return_value = None
        datastore_mock.deleteStory("1")
        datastore_mock.deleteStory.assert_called_once_with("1")
        backlog = IBacklog(datastore_mock)
        self.assertRaises(StoryNotFoundError, backlog.Remove, "1")

    def _getFakeStoryList1(self):
        # Total points of all stories is 45.
        self.story1 = story1 = Story("1", 3, 1)
        self.story2 = story2 = Story("2", 13, 1)
        self.story3 = story3 = Story("3", 1, 3)
        self.story4 = story4 = Story("4", 3, 10)
        self.story5 = story5 = Story("5", 20, 3)
        self.story6 = story6 = Story("6", 5, 3)
        return [story1, story2, story3, story4, story5, story6]

    def test_getSprintNegativeInput(self):
        # Make sure IBacklog.getSprint returns [] for negative totalPointsAchievable input.
        storylist = self._getFakeStoryList1()
        datastore_mock = Mock()
        datastore_mock.__class__ = IDatastore
        datastore_mock.readStory.return_value = storylist
        backlog = IBacklog(datastore_mock)
        actual_storylist = backlog.getSprint(-1)
        self.assertEqual(actual_storylist, [])
  
    def test_getSprintExpectAllStories(self):
        # Make sure IBacklog.getSprint returns all the stories when totalPointsAchievable input
        # is greater than the total points of all the stories.
        storylist = self._getFakeStoryList1()
        datastore_mock = Mock()
        datastore_mock.__class__ = IDatastore
        datastore_mock.readStory.return_value = storylist
        backlog = IBacklog(datastore_mock)
        actual_storylist= backlog.getSprint(46)
        self.assertEqual(storylist, actual_storylist)

    def test_getSprintAllPointsTooHigh(self):
        # Make sure IBacklog.getSprint returns [] when all stories have Point value higher than
        # totalPointsAchievable input.
        storylist = self._getFakeStoryList1()
        datastore_mock = Mock()
        datastore_mock.__class__ = IDatastore
        datastore_mock.readStory.return_value = storylist
        backlog = IBacklog(datastore_mock)
        actual_storylist = backlog.getSprint(10)
 
    def test_getSprintNormal1(self):
        # Make sure IBacklog.getSprint returns the maximum stories for totalPointsAchievable input.
        # Lower Priority number is more important.
        # Maximize lower Priority first, than higher Priorities.
        storylist = self._getFakeStoryList1()
        datastore_mock = Mock()
        datastore_mock.__class__ = IDatastore
        datastore_mock.readStory.return_value = storylist
        backlog = IBacklog(datastore_mock)
        actual_storylist = backlog.getSprint(10)
        self.assertIn(self.story1, actual_storylist)
        self.assertIn(self.story3, actual_storylist)
        self.assertIn(self.story6, actual_storylist)


if __name__ == '__main__':
    unittest.main()




