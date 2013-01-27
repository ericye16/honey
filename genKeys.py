#!/usr/bin/env python3

import csv, random, sys

numStudents = 73

students = []

student_emails_file = open("Class.csv")
student_emails = csv.reader(student_emails_file)
next(student_emails) #get rid of the header row
# Remember: each row is in 'First Name', 'Last name', 'email' format


for i in student_emails:
    #make a list of tuples between firstnames, emails and bits
    students.append((i[0], i[2], random.getrandbits(32)))

outfile = open('keys.secret', 'w')
student_emails_file.close()
writer = csv.writer(outfile)
writer.writerows(students)
outfile.close()
