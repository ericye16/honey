from __future__ import print_function
from google.appengine.ext.remote_api import remote_api_stub
import honey
import getpass

def auth_func():
    return (raw_input('Username:'), getpass.getpass('Password:'))

remote_api_stub.ConfigureRemoteApi(None, '/_ah/remote_api', auth_func,
                                   'topsnight13.appspot.com')

##code

def addVote(person, numPts, d):
    if person in d:
        d[person] += numPts
    else:
        d[person] = numPts

peopleAndVotes = {} # A dict matching people to the number of points
#scoring system: 1st choice: 3, 2nd choice: 2, 3rd choice: 1

votes = honey.Vote.all()
for vote in votes.run():
    addVote(vote.firstChoice, 3, peopleAndVotes)
    addVote(vote.secondChoice, 2, peopleAndVotes)
    addVote(vote.thirdChoice, 1, peopleAndVotes)
    
for vote in sorted(peopleAndVotes, key=lambda x: peopleAndVotes[x], reverse=True):
    print("%s: %d" % (vote, peopleAndVotes[vote]))
