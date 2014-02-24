IBacklog 
==============
A coding excercise python3 module for managing Story objects with an IBacklog interface.

In real life, I probably would have written this in Django, but for a coding exercise 
I don't think that would show much.

### Requirements
sqlite3

### Example output
Run it from the command line
$ python3 ibacklog.py

### Usage
Load the module and get the backlog object:
```
>>> from ibacklog import *
>>> backlog = IBacklog(SQLLiteDatastore())
```

Make some stories:
```
>>> story1 = Story("1", 3, 1)
>>> story2 = Story("2", 13, 1)
>>> story3 = Story("3", 8, 3)
>>> story4 = Story("4", 3, 10)
>>> story5 = Story("5", 20, 3)
>>> story6 = Story("6", 5, 3)
```

Add the stories to the datastore:
```
>>> backlog.Add(story1)
>>> backlog.Add(story2)
>>> backlog.Add(story3)
>>> backlog.Add(story4)
>>> backlog.Add(story5)
>>> backlog.Add(story6)
```

See all the stories been added:
```
>>> storylist = backlog.getSprint(100)
>>> print(storylist)
[Story 2: (Pr1 Pts13), Story 1: (Pr1 Pts3), Story 5: (Pr3 Pts20), Story 3: (Pr3 Pts8), Story 6: (Pr3 Pts5), Story 4: (Pr10 Pts3)]
```

getSprint returns an empty list if we don't set the totalPointsAchievable high enough:
```
>>> storylist = backlog.getSprint(1)
>>> print(backlog.getSprint(1))
[]
```

getSprint chooses stories with lower priority first:
```
>>> storylist = backlog.getSprint(3)
>>> print(storylist)
[Story 1: (Pr1 Pts3)]
```

getSprint maximizes the Points first choosing for priority:
```
>>> storylist = backlog.getSprint(13)
>>> print(storylist)
[Story 2: (Pr1 Pts13)]
```

Remove returns the story if it is in the datatore:
```
>>> story = backlog.Remove("1")
>>> print(story)
Story 1: (Pr1 Pts3)
```

Now the story is removed:
```
>>> storylist = backlog.getSprint(100)
>>> print(storylist)
[Story 2: (Pr1 Pts13), Story 5: (Pr3 Pts20), Story 3: (Pr3 Pts8), Story 6: (Pr3 Pts5), Story 4: (Pr10 Pts3)]
```

