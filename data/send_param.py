from flask_wtf import FlaskForm
from wtforms import PasswordField, BooleanField, SubmitField, IntegerField
from wtforms import EmailField
from wtforms.validators import DataRequired


class Send_param(FlaskForm):
    light_on = IntegerField('Порог включения освещения', validators=[DataRequired()])
    heat_on = IntegerField('Температура включения подогрева', validators=[DataRequired()])
    heat_off = IntegerField('Температура выключения подогрева', validators=[DataRequired()])
    fan_on = IntegerField('Температура включения вентилятора', validators=[DataRequired()])
    pump_on = IntegerField('Порог включения насоса', validators=[DataRequired()])
    water = IntegerField('Порог низкого уровня воды', validators=[DataRequired()])
    delta_loop = IntegerField('Частота опроса теплицей параметров', validators=[DataRequired()])
    delta_send = IntegerField('Частота отправки параметров', validators=[DataRequired()])
    submit = SubmitField('Отправить')
