from news_app import db

class Timeline(db.Model):
    __tablename__ = 'timeline'

    id = db.Column(db.Integer, primary_key=True)
    headline = db.Column(db.Text, unique=True)
    link = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f"Timeline {self.id}, {self.headline}"