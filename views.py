from flask import render_template, url_for, jsonify

from . import app
from .models import Base


@app.get('/')
def index():
    numbers = Base.query.all()
    return render_template('index.html', nums=numbers)


@app.get('/get_db')
def get_db():
    result = [{'date': item.datetime,
               'num': item.num,
               'crop': item.crop,
               'image': item.image} for item in Base.query.all()]
    return jsonify(db=result, status=200)
