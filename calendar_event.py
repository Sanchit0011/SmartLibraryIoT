# Reference: https://developers.google.com/calendar/quickstart/python
# Documentation: https://developers.google.com/calendar/overview

# Import the necessary modules
from __future__ import print_function
from datetime import datetime
from datetime import timedelta
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

# Defined the calendar_event class
class calendar_event:
    """The calendar_event class is used to add or delete events for return of books 
    from google calendar, based on whether a book has been borrowed or returned."""

    # Building google calendar service connection 
    SCOPES = "https://www.googleapis.com/auth/calendar"
    store = file.Storage("token.json")
    creds = store.get()
    if(not creds or creds.invalid):
        flow = client.flow_from_clientsecrets("credentials.json", SCOPES)
        creds = tools.run_flow(flow, store)
    service = build("calendar", "v3", http=creds.authorize(Http()))
    
    # Function to add google calendar event one week from today when book is borrowed
    def insert(self, book_title, book_id):
        """This method inserts a new google calendar event for the return of a book whenever 
        a book is borrowed. The event is added one week from the current date.
        
        Arguments:
            book_title {string} -- The title of the book to be specified in return book google calendar event.
            book_id {int} -- The id of the book to be specified in return book google calendar event.
        """
        # Setting current date
        date = datetime.now()
        
        # Setting event to added one week from current date 
        next_week = (date + timedelta(days = 7)).strftime("%Y-%m-%d")
        time_start = "{}T06:00:00+10:00".format(next_week)
        time_end = "{}T07:00:00+10:00".format(next_week)
        
        # Specifying event details 
        event = {
            "summary": str(book_id) + ":" + " " + book_title + " Return Due Date",
            "location": "Library",
            "description": "Adding new book return event",
            "start": {
                "dateTime": time_start,
                "timeZone": "Australia/Melbourne",
            },
            "end": {
                "dateTime": time_end,
                "timeZone": "Australia/Melbourne",
            },
            "reminders": {
                "useDefault": False,
                "overrides": [
                    { "method": "email", "minutes": 5 },
                    { "method": "popup", "minutes": 10 },
                ],
            }
        }
        
        # Adding event to google calendar
        event = self.service.events().insert(calendarId = "primary", body = event).execute()
        print("Event created: {}".format(event.get("htmlLink")))

     # Function to delete google calendar event when book gets returned
    def delete(self, book_id):
        """This method deletes a google calendar event for the return of a book when the book
        is returned, using the book id to match the event.
        
        Arguments:
            book_id {int} -- The id of the book returned
        """
        # Getting all events in google calendar after today 
        now = datetime.utcnow().isoformat() + "Z" # "Z" indicates UTC time.
        print("Getting all events.")
        events_result = self.service.events().list(calendarId = "primary", timeMin = now,
        singleEvents = True, orderBy = "startTime").execute()
        events = events_result.get("items", [])
        
        # Looping through all events and deleting event for book returned
        for event in events:
            b_id = event['summary'].split(':')
            if(int(b_id[0]) == book_id):
                event_id = event.get('id') 
                self.service.events().delete(calendarId='primary', eventId=event_id).execute()
                print("Event deleted")
                break










