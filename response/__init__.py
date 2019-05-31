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
  booking_date = booking_date[0:10]
  try:
    if db.check_date(booking_date):
      response_obj = [{"text": {"text": ["The time slot your looking for ?"]}},{"card": {"title": "The time slot your looking for ?","buttons": []},"platform": "TELEGRAM"}]
      if db.free_slot1(booking_date):
        response_obj[1]['card']['buttons'].append({ "text" : "5PM-6PM" })
      if db.free_slot2(booking_date):
        response_obj[1]['card']['buttons'].append({ "text" : "6PM-7PM" })
      if db.free_slot3(booking_date):
        response_obj[1]['card']['buttons'].append({ "text" : "7PM-8PM" })
      return response_obj
    else:
      return [{"text": {"text": ["Every slots are filled in the mentioned date, can you try someother day ?"]}},{"text": {"text": ["Every slots are filled in the mentioned date, can you try someother day ?"]},"platform": "TELEGRAM"}]
  except ConnectionError:
    return [{"text": {"text": ["Sorry something went wrong. Try again later."]}},{"text": {"text": ["Sorry something went wrong. Try again later."]},"platform": "TELEGRAM"}]

def get_timeslots(req):
  booking_date = req['queryResult']['outputContexts'][1]['parameters']['date']
  start_time = req['queryResult']['parameters']['time-period']['startTime']
  start_time = int(start_time[11:13])-12
  booking_date = booking_date[0:10]
  time_slot1 = str(start_time)+':00 PM'
  time_slot2 = str(start_time)+':30 PM'
  response_obj = [{"text": {"text": ["The time your looking for ?"]}},{"card": {"title": "The time your looking for ?","buttons": []},"platform": "TELEGRAM"}]
  slots = ['slot1', 'slot2', 'slot3']
  time_period = [5,6,7]
  slot = slots[time_period.index(start_time)]
  try:
    if db.free_time1(booking_date, slot):
      response_obj[1]['card']['buttons'].append({ "text" : "{0}".format(time_slot1) })
    if db.free_time2(booking_date, slot):
      response_obj[1]['card']['buttons'].append({ "text" : "{0}".format(time_slot2) })
    return response_obj
  except ConnectionError:
    return [{"text": {"text": ["Sorry something went wrong. Try again later."]}},{"text": {"text": ["Sorry something went wrong. Try again later."]},"platform": "TELEGRAM"}]

def get_time(req):
  booking_date = req['queryResult']['outputContexts'][1]['parameters']['date']
  booking_time = req['queryResult']['parameters']['time']
  booking_date = booking_date[0:10]
  slots = ['slot1', 'slot2', 'slot3']
  time_period = [5,6,7]
  slot = slots[time_period.index(int(booking_time[11:13])-12)]
  timings = [0,30]
  time_slot = timings.index(int(booking_time[14:16]))
  try:
    db.book_table(booking_date, time_slot, slot)
    return [{"text": {"text": ["Can I have your Email Id for confirming your reservation!"]}},{"text": {"text": ["Can I have your Email Id for confirming your reservation!"]},"platform": "TELEGRAM"}]
  except ConnectionError:
    return [{"text": {"text": ["Sorry something went wrong. Try again later."]}},{"text": {"text": ["Sorry something went wrong. Try again later."]},"platform": "TELEGRAM"}]

def get_event_note(req):
  booking_note = req['queryResult']['queryText']
  booking_date = req['queryResult']['outputContexts'][1]['parameters']['date']
  booking_time = req['queryResult']['outputContexts'][1]['parameters']['time']
  booking_email = req['queryResult']['outputContexts'][1]['parameters']['email']
  booking_date = booking_date[0:10]
  booking_time = booking_time[11:16]
  try:
    db.book_note(booking_date, booking_time, booking_note)
    special_event = True
    background_process(booking_date, booking_time, booking_email, special_event)
    return [{"text": {"text": ["Reservation is completed successfully for your special event and confirmation will be send to your mail"]}},{"text": {"text": ["Reservation is completed successfully for your special event and confirmation will be send to your mail"]},"platform": "TELEGRAM"}]
  except ConnectionError:
    return [{"text": {"text": ["Sorry something went wrong. Try again later."]}},{"text": {"text": ["Sorry something went wrong. Try again later."]},"platform": "TELEGRAM"}]

def get_event_negative_response(req):
  booking_date = req['queryResult']['outputContexts'][1]['parameters']['date']
  booking_time = req['queryResult']['outputContexts'][1]['parameters']['time']
  booking_email = req['queryResult']['outputContexts'][1]['parameters']['email']
  special_event = False
  try:
    background_process(booking_date, booking_time, booking_email, special_event)
    return [{"text": {"text": ["Reservation is completed successfully and confirmation will be send to your mail"]}},{"text": {"text": ["Reservation is completed successfully and confirmation will be send to your mail"]},"platform": "TELEGRAM"}]
  except Exception:
    return [{"text": {"text": ["Sorry something went wrong. Try again later."]}},{"text": {"text": ["Sorry something went wrong. Try again later."]},"platform": "TELEGRAM"}]
