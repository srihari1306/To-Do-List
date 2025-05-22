from app import db
from werkzeug.security import generate_password_hash, check_password_hash

#stores the task
class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    
#to store user data
class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password_hash =db.Column(db.String(128), nullable=False)
    tasks = db.relationship('Task',backref='user',lazy=True) #1:many relationship
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password) #Hashes a plain text password so that it can be safely stored in a database.
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password) #Verifies whether a plain text password matches the hashed password stored in the database.

