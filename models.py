from db import db
from datetime import datetime

class Img(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    mimetype = db.Column(db.Text, nullable=False)
    file_location = db.Column(db.Text, nullable=False)
    private_img = db.Column(db.Boolean,nullable=False)


# TODO: may create an user table for access control