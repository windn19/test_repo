from datetime import datetime

from . import db


class Base(db.Model):
    datetime = db.Column(db.DateTime, primary_key=True, default=datetime.now)
    num = db.Column(db.String(9))
    crop = db.Column(db.String(30))
    image = db.Column(db.String(30))
    res = db.Column(db.Text)

    def __repr__(self):
        return f'Number - {self.datetime.strftime("%d.%m.%Y")} - {self.num}'
