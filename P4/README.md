#Developing Scalable App in Python using Google App Engine

##Objectvie
The project is a proof of my knowledege about web application development on managed cloud platform (Google App Engine)

##How to use the application
[Deployment Guide] (https://github.com/linusdong/Udacity_Nanodegree_FullStackWeb/blob/master/P4/deployment.md)

My appspot ID
```BASH
smart-impact-94201
```
To visit the front end, Click [link] (https://smart-impact-94201.appspot.com)

##Task 1: Add Sessions to a Conference
The session is a kind in datastore. It has the following properties:

    name            = ndb.StringProperty(required=True)
    speaker         = ndb.StringProperty()
    highlights      = ndb.StringProperty(repeated=True)
    typeOfSession   = ndb.StringProperty()
    startDateTime   = ndb.DateTimeProperty()
    duration        = ndb.IntegerProperty()
    organizerUserId = ndb.StringProperty()

DateTimeProperty gives more accuracy in term of quering session entities filter by date or time argument.

Speaker is a string property only. Further enhancement needed. Speaker entity could derive from user entity with extra field like a list with name "host sessions" to indicate this user is the speaker of some sessions. Then a queue task can be set up to send confirmation email to the speaker when session is created.

standard endpoints as follow:

1. [link](https://apis-explorer.appspot.com/apis-explorer/?base=https://smart-impact-94201.appspot.com/_ah/api#p/conference/v1/conference.getConferenceSessions) to getConferenceSessions(websafeConferenceKey)
1. [link](https://apis-explorer.appspot.com/apis-explorer/?base=https://smart-impact-94201.appspot.com/_ah/api#p/conference/v1/conference.getConferenceSessionsByType) to getConferenceSessionsByType(websafeConferenceKey, typeOfSession)
1. [link](https://apis-explorer.appspot.com/apis-explorer/?base=https://smart-impact-94201.appspot.com/_ah/api#p/conference/v1/conference.getSessionsBySpeaker) to getSessionsBySpeaker(speaker) 
1. [link](https://apis-explorer.appspot.com/apis-explorer/?base=https://smart-impact-94201.appspot.com/_ah/api#p/conference/v1/conference.createSession) to createSession(SessionForm, websafeConferenceKey)

extra endpoints as follow:

* querySessions(list_of_filters) -- like queryConferences, reuse _formatFilters(filters)

``` 
Please follow the same principle in queryConferences.
You can query the following properties, speaker, duration, type and startDateTime.
example:
"field":"STARTDATETIME"
"operator":"GT"
"value":"2015-05-17 12:35:22"
```
