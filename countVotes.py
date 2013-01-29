from __future__ import print_function
from google.appengine.ext.remote_api import remote_api_stub
import honey
import getpass
import sys

# Usage: python countVotes.py fdsfdsfds > results.html

def auth_func():
    print("Username:", end='', file=sys.stderr)
    return (raw_input(),
            getpass.getpass('Password:', sys.stderr))

remote_api_stub.ConfigureRemoteApi(None, '/_ah/remote_api', auth_func,
                                   'topsnight13.appspot.com')

##code

if len(sys.argv) > 1:
    printHTML = True
else:
    printHTML = False

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

if printHTML:
    HTMLHead = '''
<!DOCTYPE html>
<head>
  <link type="text/css" rel="stylesheet" href="stylesheets/results.css">
  <title>Vote Results</title>
</head>
<body>
  <h1>Vote Results</h1>
  <table>
    <tr>
      <th class="narrow">Rank</th>
      <th>Candidate</th>
    </tr>
    <!--Below will be autogenerated.-->'''
    rowTemplate = '''
    <tr>
      <td class="narrow">%d</td>
      <td>%s</td>
    </tr>'''
    HTMLTail = '''
  <!--end autogeneration-->
  </table>
  <p class="footnote">*A first choice is assigned 3 points,
  second choice 2 points, and third choice 1 point.</p>
</body>'''
    print(HTMLHead)

rank = 1
    
for vote in sorted(peopleAndVotes,
                   key=lambda x: peopleAndVotes[x], reverse=True):
    if printHTML:
        print(rowTemplate % (rank, vote))
    else:
        print("%s: %d" % (vote, peopleAndVotes[vote]))
    rank += 1

if printHTML:
    print(HTMLTail)
