#Developing Scalable App in Python using Google App Engine

##Objectvie
The project is a proof of my knowledege about web application development on managed cloud platform (Google App Engine)

##How to use the application
[Deployment Guide](https://github.com/linusdong/Udacity_Nanodegree_FullStackWeb/blob/master/P4/deployment.md)

My appspot ID
```BASH
smart-impact-94201
```
To visit the front end, Click [link](https://smart-impact-94201.appspot.com)

##Change Log
May 25th 2015,
* add checking function to make sure urlsafe_key is conference key
* add validation_helper.py

May 24th 2015, 
* updated session data model
* added different ResouceContainers for varies request
* refactor some URL paths
* added transactional method on _sessionRegistration function to prevent race condition
* added new query getRecentConferences

May 14th 2015, 
* basic requirement completed.

##Task 1: Add Sessions to a Conference
The session is a kind in datastore. It has the following properties:

    name            = ndb.StringProperty(required=True)
    speaker         = ndb.StringProperty()
    highlights      = ndb.StringProperty(repeated=True)
    typeOfSession   = ndb.StringProperty()
    startDateTime   = ndb.DateTimeProperty()
    duration        = ndb.IntegerProperty()

###Model Explaination

When a session entity is created, a parent is set to conference entity. Same as conference entity is link to user profile entity. The ancestor path for session entity can help us to find root user or parent conference that related to session.

DateTimeProperty gives more accuracy in term of quering session entities filter by date or time argument.

Speaker is a string property only. Further enhancement needed. Speaker entity could derive from user entity with extra field like a list with name "host sessions" to indicate this user is the speaker of some sessions. Then a queue task can be set up to send confirmation email to the speaker when session is created.

###standard endpoints as follow:

1. [link](https://apis-explorer.appspot.com/apis-explorer/?base=https://smart-impact-94201.appspot.com/_ah/api#p/conference/v1/conference.getConferenceSessions) to getConferenceSessions(websafeConferenceKey)
1. [link](https://apis-explorer.appspot.com/apis-explorer/?base=https://smart-impact-94201.appspot.com/_ah/api#p/conference/v1/conference.getConferenceSessionsByType) to getConferenceSessionsByType(websafeConferenceKey, typeOfSession)
1. [link](https://apis-explorer.appspot.com/apis-explorer/?base=https://smart-impact-94201.appspot.com/_ah/api#p/conference/v1/conference.getSessionsBySpeaker) to getSessionsBySpeaker(speaker) 
1. [link](https://apis-explorer.appspot.com/apis-explorer/?base=https://smart-impact-94201.appspot.com/_ah/api#p/conference/v1/conference.createSession) to createSession(SessionForm, websafeConferenceKey)

###extra endpoints as follow:

* querySessions(list_of_filters) -- like queryConferences, reuse _formatFilters(filters)

``` 
Please follow the same principle in queryConferences.
You can query the following properties, speaker, duration, type and startDateTime.
example:
"field":"STARTDATETIME"
"operator":"GT"
"value":"2015-05-17 12:35:22"
```
##Task 2: Add Sessions to User Wishlist
1. [link](https://apis-explorer.appspot.com/apis-explorer/?base=https://smart-impact-94201.appspot.com/_ah/api#p/conference/v1/conference.addSessionToWishlist) to addSessionToWishlist(SessionKey)
2. [link](https://apis-explorer.appspot.com/apis-explorer/?base=https://smart-impact-94201.appspot.com/_ah/api#p/conference/v1/conference.getSessionsInWishlist) to getSessionsInWishlist()

###Model Explaination

There is property on profile model named sessionKeysWishlist. The property takes a list of values of the underlying type. This is a list of session keys as wishlist in user model. User can only add session in the conference that user have registered to attend.

##Task 3: Work on indexes and queries

### addtional endpoints

1. [link](https://apis-explorer.appspot.com/apis-explorer/?base=https://smart-impact-94201.appspot.com/_ah/api#p/conference/v1/conference.queryConferenceSessionsByLongDuration) to queryConferenceSessionsByLongDuration(websafeConferenceKey)
1. [link](https://apis-explorer.appspot.com/apis-explorer/?base=https://smart-impact-94201.appspot.com/_ah/api#p/conference/v1/conference.queryConferenceSessionsByShortDuration) to queryConferenceSessionsByShortDuration(websafeConferenceKey)
1. [link](https://apis-explorer.appspot.com/apis-explorer/?base=https://smart-impact-94201.appspot.com/_ah/api#p/conference/v1/conference.querySessions) to querySessions (answer to query related problem)
1. [link](https://apis-explorer.appspot.com/apis-explorer/?base=https://smart-impact-94201.appspot.com/_ah/api#p/conference/v1/conference.getConferencesRecent) to getConferencesRecent

###Solve the following query related problem
####Question
Let’s say that you don't like workshops and you don't like sessions after 7 pm. How would you handle a query for all non-workshop sessions before 7 pm? What is the problem for implementing this query? What ways to solve it did you think of?

###Problem encounter
1. All session are not in the same timezone, if you assume the session time is local time, then we can treat the hour as integer, problem soloved. if the type of timestamp in each session startDateTime property is UTC, then we have to convert each UTC timestamp object to local time object(where the conference held) then compare with the value we want.

* The best way to deal with the problem is put valadation mechanism on front end to ensure user input is legit and inform the user input is localized.

1. The Datastore enforces some restrictions on queries. Violating these will cause it to raise exceptions. For example, combining too many filters, using inequalities for multiple properties, or combining an inequality with a sort order on a different property are all currently disallowed. Also filters referencing multiple properties sometimes require secondary indexes to be configured.

* The workaround is equalities for multiple properties. We can look for "typeOfSession == 'lecture' AND typeOfSession == 'demo'" (assume we only and three type of session), or we can use IN operation. See Option 2 for more detail.

####Answer
Option 1, use Session property(startDateTime) as is.

```python
        sess = Session.query()
        sess = sess.filter(Session.typeOfSession != "workshop")
        temp = []
        for session in sess:
            # we assume local time
            if session.startDateTime.hour < 19:
                temp.append(session)
        return temp
```
The reason that the data has been filtered this way is, the datetime property of session entity does not have "hour" attribute as datetime object in python.

Option 2, modify Session property, add hour property(same as month property in conference entity)

```python
interestedSessionTypes = ["lecture", "demo"]
        sess = Session.query()
        sess = sess.filter(Session.typeOfSession.IN(interestedSessionTypes))
        sess = sess.filter(Session.hour < 19)
```
##Task 4: Add a Task

1. [link](https://apis-explorer.appspot.com/apis-explorer/?base=https://smart-impact-94201.appspot.com/_ah/api#p/conference/v1/conference.getFeaturedSpeaker) to getFeaturedSpeaker()
```
MEMCACHE_SPEAKER_KEY = "FEATURED_SPEAKER"
SPEAKER_TPL = ('will host the following sessions: %s')

    @staticmethod
    def _cacheSpeakerAnnouncement(sessionKey, speaker):
        """Create Announcement & assign to memcache; used by
        memcache cron job & putAnnouncement().
        """
        c_key = ndb.Key(urlsafe=sessionKey).parent()
        if c_key is None:
            announcement = "Error"
            memcache.set(MEMCACHE_SPEAKER_KEY, announcement)
            return announcement
        s = Session.query(ancestor=c_key)
        s = s.filter(Session.speaker == speaker
                     ).fetch(projection=[Session.name])
        if len(s) > 1:
            # If there is more than one session by this speaker at this conference, 
            # also add a new Memcache entry that features the speaker and session names.
            speaker_name = "Our Featured speaker {0} ".format(speaker)
            announcement = speaker_name + SPEAKER_TPL % (
                ', '.join(session.name for session in s))
            memcache.set(MEMCACHE_SPEAKER_KEY, announcement)
        else:
            # If there are no sold out conferences,
            # delete the memcache announcements entry
            announcement = ""
            memcache.delete(MEMCACHE_SPEAKER_KEY)

        return announcement


    @endpoints.method(message_types.VoidMessage, StringMessage,
            path='getFeaturedSpeaker',
            http_method='GET', name='getFeaturedSpeaker')
    def getFeaturedSpeaker(self, request):
        """Return Announcement from memcache."""
        return StringMessage(data=memcache.get(MEMCACHE_SPEAKER_KEY) or "")


        taskqueue.add(params={'sessionKey': session.websafeSessionKey,
            'speaker': session.speaker},
            url='/tasks/set_speaker_announcement'
        )
```
