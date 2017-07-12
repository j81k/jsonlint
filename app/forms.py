from flask_wtf import Form
from wtforms.fields import StringField, BooleanField, TextAreaField
from wtforms.validators import DataRequired

class LoginForm(Form):
	openid 		= StringField('openid', validators=[DataRequired()])
	remember_me = BooleanField('remember_me', default=False)


class InputForm(Form):
	duplicate_key = BooleanField('duplicate_key', default=True)
	json_inp = TextAreaField('json_inp', validators=[DataRequired()], default='{"data":{"user": "Ashok"}}')

