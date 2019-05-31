from database import RestaurantDb
from helper import background_process 

db = RestaurantDb()

def get_response(req):
  user_response = req['queryResult']['parameters']['Response']
  if user_response == 'Negative_response':
    return [{"text": { "text": [ "Thank you for your response !" ] }, "platform": "TELEGRAM" }, { "text": { "text": [ "Thank you for your response !" ] } } ]
  else:
    return [{"text": { "text": [ "The date your looking for ?" ] }, "platform": "TELEGRAM" }, { "text": { "text": [ "The date your looking for ?" ] } } ]

def get_date(req):
  booking_date = req['queryResult']['outputContexts'][0]['parameters']['date']
  if db.check_date(booking_date):
    response_obj = db.free_slots(booking_date)
    return response_obj
  else:
    return [{"text": {"text": ["Every slots are filled in the mentioned date, can you try someother day ?"]}},{"text": {"text": ["Every slots are filled in the mentioned date, can you try someother day ?"]},"platform": "TELEGRAM"}]

def get_timeslots(req):
  booking_date = req['queryResult']['outputContexts'][1]['parameters']['date']
  start_time = req['queryResult']['parameters']['time-period']['startTime']
  response_obj = db.free_time(booking_date, start_time)
  return response_obj

def get_time(req):
  booking_date = req['queryResult']['outputContexts'][1]['parameters']['date']
  booking_time = req['queryResult']['parameters']['time']
  db.book_table(booking_date, booking_time)
  return [{"text": {"text": ["Can I have your Email Id for confirming your reservation!"]}},{"text": {"text": ["Can I have your Email Id for confirming your reservation!"]},"platform": "TELEGRAM"}]

def get_email():
  return [{"text": {"text": ["Do you have any special event ?"]}},{"text": {"text": ["Do you have any special event ?"]},"platform": "TELEGRAM"}]

def get_event_positive_response():
  return [{"text": {"text": ["Mention your special event note"]}},{"text": {"text": ["Mention your special event note"]},"platform": "TELEGRAM"}]

def get_event_note(req):
  booking_note = req['queryResult']['queryText']
  booking_date = req['queryResult']['outputContexts'][1]['parameters']['date']
  booking_time = req['queryResult']['outputContexts'][1]['parameters']['time']
  booking_email = req['queryResult']['outputContexts'][1]['parameters']['email']
  db.book_note(booking_date, booking_time, booking_note)
  special_event = True
  background_process(booking_date, booking_time, booking_email, special_event)
  return [{"text": {"text": ["Reservation is completed successfully for your special event and confirmation will be send to your mail"]}},{"text": {"text": ["Reservation is completed successfully for your special event and confirmation will be send to your mail"]},"platform": "TELEGRAM"}]

def get_event_negative_response(req):
  booking_date = req['queryResult']['outputContexts'][1]['parameters']['date']
  booking_time = req['queryResult']['outputContexts'][1]['parameters']['time']
  booking_email = req['queryResult']['outputContexts'][1]['parameters']['email']
  special_event = False
  background_process(booking_date, booking_time, booking_email, special_event)
  return [{"text": {"text": ["Reservation is completed successfully and confirmation will be send to your mail"]}},{"text": {"text": ["Reservation is completed successfully and confirmation will be send to your mail"]},"platform": "TELEGRAM"}]
