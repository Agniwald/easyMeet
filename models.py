from main import db


class Subject(db.ModelView):
	__tablename__ = "Subjects"
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String, unique=True, nullable=True)
	url = db.Column(db.String, unique=True, nullable=True)

	def __repr__(self):
		return self.name


class ActiveTimer(db.ModelView):
	__tablename__ = "ActiveTimers"
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String, unique=True, nullable=True)
	url = db.Column(db.String, unique=True, nullable=True)
	start = db.Column(db.DateTime, unique=True, nullable=True)
	end = db.Column(db.DateTime, unique=True, nullable=True)

	def __repr__(self):
		return f"{self.name} - {self.start} to {self.end}"
