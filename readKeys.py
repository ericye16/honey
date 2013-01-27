from google.appengine.ext.remote_api import remote_api_stub
import honey
import getpass
import csv

def auth_func():
    return (raw_input('Username:'), getpass.getpass('Password:'))

remote_api_stub.ConfigureRemoteApi(None, '/_ah/remote_api', auth_func,
                                   'localhost:8080')

##code
keysFile = open('keys.secret')
keysCSV = csv.reader(keysFile)
for keyRow in keysCSV:
    print keyRow
    person = honey.Person(
        email = keyRow[1],
        key_ = int(keyRow[2]))
    person.put()

keysFile.close()
