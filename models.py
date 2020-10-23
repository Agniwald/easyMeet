from app import db
from datetime import datetime
import threading


class Subject(db.Model):
	__tablename__ = "Subjects"
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String, unique=True, nullable=True)
	url = db.Column(db.String, unique=True, nullable=True)

	def __init__(self, name, url):
		self.name = name
		self.url = url

	def __repr__(self):
		return self.name


class ActiveTimer(db.Model):
	__tablename__ = "ActiveTimers"
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String, nullable=True)
	start = db.Column(db.DateTime, nullable=True)
	end = db.Column(db.DateTime, nullable=True)

	def __init__(self, name, start, end, thread_id=None):
		self.name = name
		self.start = start
		self.end = end

	@property
	def thread_id(self):
		if self.thread_id == None:
			return len(threading.enumerate()) + 1
		else:
			return self.thread_id
			
	@property
	def status(self):
		now = datetime.now()
		if self.start > now:
			return 'Waiting'
		elif self.start < now and self.end > now:
			return 'In progress'
		else:
			return 'Completed'

	def __repr__(self):
		return f"{self.name} - {self.start} to {self.end}"
