from datetime import datetime
import enum
from .db import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    tasks = db.relationship("Task", backref="user", lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class TaskStatus(str, enum.Enum):
    STARTED = "Started"
    COMPLETED = "Completed"
    PROGRESS = "In-Progress"
    READY = "Ready-to-go"

    def __str__(self):
        return self.value
    
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    notes = db.Column(db.Text, nullable=True)
    start_time = db.Column(db.DateTime, nullable=True)
    end_time = db.Column(db.DateTime, nullable=True)
    duration = db.Column(db.Integer, nullable=True)
    status = db.Column(db.Enum(TaskStatus), nullable=False, default=TaskStatus.READY)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
