from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Phrase(db.Model):
     __tablename__ = 'phrases'

     id = db.Column(db.Integer, primary_key=True)
     phrase = db.Column(db.String, nullable=False)
     meaning = db.Column(db.String, nullable=True)
     phrase_type = db.Column(db.String, nullable=True)
     note = db.Column(db.String, nullable=True)

     examples = db.relationship('Example', backref='phrase', lazy=True)

     def __repr__(self):
          return f"<Phrase {self.phrase}>"
     
class Example(db.Model):
     __tablename__ = 'examples'

     id = db.Column(db.Integer, primary_key=True)
     content = db.Column(db.Text, nullable=True)
     phrase_id = db.Column(db.Integer, db.ForeignKey('phrases.id'), nullable=False)
     
     def __repr__(self):
          return f"{super().__repr__()}"