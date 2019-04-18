from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

class SearchForm(FlaskForm):
    find = StringField('What kind of food are you looking for?', validators=[DataRequired(), Length(min=2)])
    near = StringField('Location?', validators=[DataRequired(), Length(min=2)])
    submit = SubmitField('Search')