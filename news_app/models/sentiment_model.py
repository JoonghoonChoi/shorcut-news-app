from news_app import db

class Sentiment(db.Model):
    __tablename__ = 'sentiment'

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(32))
    timeline_headline = db.Column(db.Text, db.ForeignKey('timeline.headline'))
    timeline = db.relationship('Timeline', backref='sentiment', cascade='all, delete')

    def __repr__(self):
        return f"Sentiment {self.id}, {self.type}"
