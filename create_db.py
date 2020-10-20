#!/usr/bin/python
# -*- coding: utf-8 -*-

# For development usage only #

from models import db, Subject, ActiveTimer
import datetime

db.drop_all()
db.create_all()

subjects = [("AI", "https://meet.google.com/lookup/avpbh56vxm"), ("Curcuits", "https://meet.google.com/lookup/fscfby45fe")]
timers = [("AI", datetime.datetime(2020, 10, 17, 13, 39, 0), datetime.datetime(2020, 10, 17, 13, 40, 0)), 
("Curcuits", datetime.datetime(2020, 11, 17, 13, 50, 0), datetime.datetime(2020, 11, 17, 13, 51, 0))]

for s in subjects:
	db.session.add(Subject(*s))

for t in timers:
	db.session.add(ActiveTimer(*t))

db.session.commit()
