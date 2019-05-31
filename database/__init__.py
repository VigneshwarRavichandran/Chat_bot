import MySQLdb

class RestaurantDb():
  def __init__(self):
    self.host = 'localhost'
    self.user = 'root'
    self.passwd = '1998'
    self.db = 'restaurant_bot'
    self.conn = None
    self.cur = None

  def db_connect(self):
    self.conn = MySQLdb.connect(host= self.host, user = self.user, passwd = self.passwd, db = self.db)
    self.cur = self.conn.cursor()

  def check_date(self, booking_date):
    self.db_connect()
    result = self.cur.execute("SELECT * FROM booking WHERE date = '{0}'".format(booking_date))
    if result == 0:
      self.cur.execute("INSERT INTO booking(date, slot1, slot2, slot3) VALUES('{0}', JSON_ARRAY(true, true, true), JSON_ARRAY(true, true, true), JSON_ARRAY(true, true, true))".format(booking_date))
      self.conn.commit()
    free_timeslot = self.cur.execute("SELECT * FROM booking WHERE date = '{0}' AND (JSON_EXTRACT(slot1, '$[2]') OR JSON_EXTRACT(slot2, '$[2]') OR JSON_EXTRACT(slot3, '$[2]'))".format(booking_date))
    if free_timeslot != 0:
      return True
    return False

  
  def free_slot1(self, booking_date):
    self.db_connect()
    result = self.cur.execute("SELECT * FROM booking WHERE date = '{0}' AND JSON_EXTRACT(slot1, '$[2]')".format(booking_date))
    if result != 0:
      return True
    return False

  def free_slot2(self, booking_date):
    self.db_connect()
    result = self.cur.execute("SELECT * FROM booking WHERE date = '{0}' AND JSON_EXTRACT(slot2, '$[2]')".format(booking_date))
    if result != 0:
      return True
    return False

  def free_slot3(self, booking_date):
    self.db_connect()
    result = self.cur.execute("SELECT * FROM booking WHERE date = '{0}' AND JSON_EXTRACT(slot3, '$[2]')".format(booking_date))
    if result != 0:
      return True
    return False

  def free_time1(self, booking_date, slot):
    self.db_connect()
    result = self.cur.execute("SELECT * FROM booking WHERE date = '{0}' AND JSON_EXTRACT({1}, '$[0]')".format(booking_date, slot))
    if result != 0:
      return True
    return False

  def free_time2(self, booking_date, slot):
    self.db_connect()
    result = self.cur.execute("SELECT * FROM booking WHERE date = '{0}' AND JSON_EXTRACT({1}, '$[1]')".format(booking_date, slot))
    if result != 0:
      return True
    return False

  def book_table(self, booking_date, time_slot, slot):
    self.db_connect()
    self.cur.execute("UPDATE booking SET {0} = JSON_SET({0}, '$[{2}]', false) WHERE date = '{1}'".format(slot, booking_date, time_slot))
    self.cur.execute("UPDATE booking SET {0} = JSON_SET({0}, '$[2]', false) WHERE date = '{1}' AND (NOT JSON_EXTRACT({0}, '$[0]')) AND (NOT JSON_EXTRACT({0}, '$[1]'))".format(slot, booking_date))
    self.conn.commit()

  def book_note(self, booking_date, booking_time, booking_note):
    self.db_connect()
    self.cur.execute("INSERT INTO booking_note(date, time, note) VALUES('{0}', '{1}', '{2}')".format(booking_date, booking_time, booking_note))
    self.conn.commit()

  def close(self):
    self.cur.close()
    self.conn.close()
    