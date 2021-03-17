from flask_login import UserMixin
from app import login_manager
from app import db

# Database Model -->
class UserInfo(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))

    # Constructor -->
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password


@login_manager.user_loader
def load_user(user_id):
    return UserInfo.query.get(int(user_id))

# db.create_all()  # Run this once to initialize database.

# -- Adding new data to the database -->
# data = UserInfo('Oredola street', '0908766')
# db.session.update(data) 
# db.session.commit()