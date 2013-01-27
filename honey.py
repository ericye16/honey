#!/usr/bin/env python
import datetime
import webapp2
import jinja2
import os

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

from google.appengine.ext import db

class Person(db.Model):
    """Models a person, with an email and a key."""
    email = db.EmailProperty()
    key_ = db.IntegerProperty()
    alreadyVoted = db.BooleanProperty(default=False)

class Vote(db.Model):
    """Models a single vote, consisting of three choices."""
    firstChoice = db.StringProperty()
    secondChoice = db.StringProperty()
    thirdChoice = db.StringProperty()

class BackupVote(db.Model):
    """So we have a log of things. Not to be used unless something goes
    catastrophically wrong."""
    email = db.EmailProperty()
    firstChoice = db.StringProperty()
    secondChoice = db.StringProperty()
    thirdChoice = db.StringProperty()
    date = db.DateTimeProperty(auto_now_add=True)
    

class MainPage(webapp2.RequestHandler):
    def get(self):
        # this is really just a static page
        template = jinja_environment.get_template('index.html')
        self.response.out.write(template.render({}))

class SubmitPage(webapp2.RequestHandler):
    def post(self):
        personEmail = self.request.get('emailGiven')
        try:
            personKey = int(self.request.get('key'))
        except:
            #replace this later
            self.response.out.write("Your key was not a number. Try again.")
            return

        # Check if the email and key are right
        person = Person.all()
        person.filter("email =", personEmail)
        person.filter("key_ =", personKey)
        if person.count() < 1:
            template = jinja_environment.get_template('mismatch_error.html')
            self.response.out.write(template.render({}))
            return

        voter = person.get()
        # Check if they've already voted
        if voter.alreadyVoted:
            template = jinja_environment.get_template('already_voted.html')
            self.response.out.write(template.render({}))
            return

        # At this point, they have been validated.
        voter.alreadyVoted = True
        voter.put()
        firstChoice = self.request.get("choice1")
        secondChoice = self.request.get("choice2")
        thirdChoice = self.request.get("choice3")
        backup_vote = BackupVote(
            email=personEmail, firstChoice=firstChoice,
            secondChoice=secondChoice, thirdChoice=thirdChoice)
        backup_vote.put()

        vote = Vote(firstChoice=firstChoice, secondChoice=secondChoice,
                    thirdChoice=thirdChoice)
        vote.put()
        template = jinja_environment.get_template('successfully_voted.html')
        self.response.out.write(template.render({}))

app = webapp2.WSGIApplication([('/', MainPage),
                               ('/submit', SubmitPage)],
                               debug=True)
