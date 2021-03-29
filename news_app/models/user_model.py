from news_app import db

class User(db.Model):
    __tablename__ : 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), nullable=False)
    location = db.Column(db.String(64))
    timelines = db.relationship('Timeline', backref='user', cascade='all, delete')

    def __repr__(self):
        return f"User {self.id}, {self.username}"