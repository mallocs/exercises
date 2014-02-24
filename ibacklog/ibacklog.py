
import sqlite3

SQLITE_DB_FILENAME = 'ibacklog.db'
DB_TABLE_NAME = 'Stories'


class StoryNotFoundError(Exception):
    def __init__(self, message):
        self.message = message

class IDatastore():
    def createStory(self, s):
        pass

    def readStory(self):
        pass

    def deleteStory(self, Id):
        pass


class SQLLiteDatastore(IDatastore):
    def __init__(self, db_filename=SQLITE_DB_FILENAME):
        IDatastore.__init__(self)
        self.conn = sqlite3.connect(db_filename)
        self._execute('''CREATE TABLE IF NOT EXISTS ''' + DB_TABLE_NAME + '''(Id TEXT, Points INTEGER, Priority INTEGER)''')

    def _execute(self, sql_cmd, close=True, bindings=None):
        with self.conn:
            self.cur = self.conn.cursor()
            if bindings:
                self.cur.execute(sql_cmd, bindings)
            else:
                self.cur.execute(sql_cmd)
            if close:
                self.conn.commit()
                self.cur.close()

    def _makeStoryFromTuple(self, tuple):
        return Story(tuple[0], tuple[1], tuple[2])

    def createStory(self, s):
        self._execute('INSERT INTO ' + DB_TABLE_NAME + '(Id, Points, Priority) VALUES(?, ?, ?)', True, (s.Id, s.Points, s.Priority))

    def readStory(self):
        self._execute('''SELECT * FROM ''' + DB_TABLE_NAME, False)
        stories_tuple_list = self.cur.fetchall()
        self.cur.close()
        return [self._makeStoryFromTuple(story) for story in stories_tuple_list]

    def deleteStory(self, Id):
        self._execute('''SELECT * FROM ''' + DB_TABLE_NAME + ''' WHERE Id=?''', False, (Id,))
        stories_tuple_list = self.cur.fetchall()
        if len(stories_tuple_list) == 1:
            self._execute('''DELETE FROM ''' + DB_TABLE_NAME + ''' WHERE Id=?''', False, (Id,))
            story = self._makeStoryFromTuple(stories_tuple_list[0])
        else:
            story = None
        self.conn.commit()
        self.cur.close()
        return story


class IBacklog:
    def __init__(self, datastore):
        if not isinstance(datastore, IDatastore):
            raise TypeError
        self.datastore = datastore

    def Add(self, s):
        if not isinstance(s, Story):
            raise TypeError
        self.datastore.createStory(s)

    def Remove(self, Id):
        story = self.datastore.deleteStory(Id)
        if not story:
            raise StoryNotFoundError("Story was not found in the datastore")
        return story

    def getSprint(self, totalPointsAchievable):
        totalPointsAchievable = int(totalPointsAchievable)
        storylist = self.datastore.readStory()
        storylist.sort(key = lambda story: (story.Priority, -story.Points))
        points = 0
        sprintlist = []
        for story in storylist:
            if points + story.Points <= totalPointsAchievable:
                points += story.Points
                sprintlist.append(story)
        return sprintlist

    def getStories(self):
        return self.datastore.readStory()


class Story:
    def __init__(self, Id, Points, Priority):
        self.Id = str(Id)
        self.Points = int(Points)
        self.Priority = int(Priority)

    def __repr__(self):
        return "Story " + self.Id + ": (Pr" + str(self.Priority) + " Pts" + str(self.Points) + ")"


#Add: Should call createStory once.
#Remove: Should call deleteStory once and return 1 story. 
#
#getSprint: Should return a list of stories. Test various input numbers given different story lists.

#Setup DB fixture

backlog = IBacklog(SQLLiteDatastore())
story1 = Story("1", 3, 1)
story2 = Story("2", 13, 1)
story3 = Story("3", 1, 3)
story4 = Story("4", 3, 10)
story5 = Story("5", 20, 3)
story6 = Story("6", 5, 3)

backlog.Add(story1)
backlog.Add(story2)
backlog.Add(story3)
backlog.Add(story4)
backlog.Add(story5)
backlog.Add(story6)
