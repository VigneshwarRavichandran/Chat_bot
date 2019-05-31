from redis import Redis
from rq import Queue
from rq_scheduler import Scheduler
from datetime import datetime
from datetime import timedelta
import datetime as dt
import time
import smtplib
from email.mime.text import MIMEText
import datetime

def background_process(booking_date, booking_time, booking_email, special_event):
	scheduler = Scheduler(connection=Redis()) # Get a scheduler for the "default" queue
	year = int(booking_date[0:4])
	month = int(booking_date[5:7])
	day = int(booking_date[8:10])
	send_time = dt.datetime(year, month, day, 16, 0, 0)
	delay_time = int(send_time.timestamp() - time.time())
	job = scheduler.schedule(scheduled_time=datetime.datetime.utcnow(), func=send_email, args=[booking_date, booking_time, booking_email, special_event], repeat=2, interval=delay_time)

def send_email(booking_date, booking_time, booking_email, special_event):
	smtp_ssl_host = 'smtp.gmail.com'
	smtp_ssl_port = 465
	username = '16jecit119@gmail.com'
	password = 'user@123'
	sender = '16jecit119@gmail.com'
	# contents for the message
	booking_msg = ''
	booking_date = booking_date[0:10]
	booking_time = booking_time[11:16]
	if special_event:
		booking_msg += 'Your have reserved a table on {0} during {1} for your special event. Foodiee restaurant is eagerly waiting for your presence.'.format(booking_date, booking_time)
	else:
		booking_msg += 'Your have reserved a table on {0} during {1}. Foodiee restaurant is eagerly waiting for your presence.'.format(booking_date, booking_time)
	msg = MIMEText(booking_msg)
	msg['Subject'] = 'FOODIEE RESTAURANT RESERVATION'
	msg['From'] = sender
	msg['To'] = booking_email
	# email connection establishment and execution
	server = smtplib.SMTP_SSL(smtp_ssl_host, smtp_ssl_port)
	server.login(username, password)
	server.sendmail(sender, booking_email, msg.as_string())
	server.quit()