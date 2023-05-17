from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class PathForm(FlaskForm):
    path_str = StringField(label='Введите путь', validators=[DataRequired(message='Поле должно быть заполнено')])
    submit = SubmitField(label='Определить')
