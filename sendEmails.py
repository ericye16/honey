#!/usr/bin/env python3

import sys, smtplib, csv, getpass
from email.mime.text import MIMEText

fromaddr = 'topsnight2013@gmail.com'
username = 'topsnight2013@gmail.com'
password = getpass.getpass('Enter the password for %s: ' % username)

keysFile = open('keys.secret')

url = 'topsnight13.appspot.com'

msgtemplate = """
Hi {firstname},

Please vote at [the amazingly stylish] {url} for TOPSNight leadership.

Use your email and secure pin as you see below:
email: {email}
pin: {hashedpin}
"""

server = smtplib.SMTP('smtp.gmail.com:587')
server.starttls()
server.login(username, password)

def sendSingleEmail(keyFileRow, server):
    hashedpin = int(keyFileRow[2])
    toEmail = keyFileRow[1]
    msg = MIMEText(msgtemplate.format(firstname=keyFileRow[0], url=url,
                             hashedpin=hashedpin, email=toEmail))
    msg['Subject'] = 'TOPSNight leadership voting'
    msg['From'] = fromaddr
    msg['To'] = toEmail
    print(msg)
    
    server.send_message(msg)

keys = csv.reader(keysFile)

for keyRow in keys:
    sendSingleEmail(keyRow, server)

server.quit()
