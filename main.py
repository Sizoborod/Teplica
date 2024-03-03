import datetime

from flask import Flask, render_template, request, redirect
import flask_restful
import requests

from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from waitress import serve
from werkzeug.utils import redirect

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
import random as ran
from data import db_session
from data.users import User
from data.sensors import Sensors
from data.login_form import LoginForm
from data.send_param import Send_param
from data.status import Status
from flask_restful import reqparse, abort, Api, Resource


db_session.global_init("teplica.db")
app = Flask(__name__)
api = flask_restful.Api(app)

app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/')
def main_window():
    return render_template('index.html')

@app.route("/map")
def map():
    map_pars = {}
    return render_template("geo.html")

@app.route("/map2")
def map2():
    map_pars = {}
    return render_template("object_manager.html")

@app.route("/r/t/<keys>")
def rucheek(keys):
    try:
        keys = keys.split('+')
        keys.extend(['0'] * 11)
        keys = keys[:11]
        url = "https://script.google.com"
        Google_ID = "AKfycbw967WZZ2KRKNg5lXlY3ox_rvrzn6qxFTZIgBXPiktHk0XLVmQLA_1jKBPRw4LGx_qW"
        url += "/macros/s/"
        url += Google_ID
        url += "/exec?temp_in="
        url += keys[0]
        url += "&h_in="
        url += keys[1]
        url += "&temp_out="
        url += keys[2]
        url += "&h_out="
        url += keys[3]
        url += "&moisture_1="
        url += keys[4]
        url += "&moisture_2="
        url += keys[5]
        url += "&light="
        url += keys[6]
        url += "&pump="
        url += keys[7]
        url += "&heat="
        url += keys[8]
        url += "&led="
        url += keys[9]
        url += "&fun="
        url += keys[10]
        r = requests.get(url)
        r.status_code
        return 'ok'



    except Exception:

        return f'NO'

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        users = db_sess.query(User).all()
        msg = (f'{user} - User.email\n{form.password.data} - form.password.data\n'
               f'{form.email.data} - form.email.data\n{users} - users')
        a = f'___ - user.check_password(form.password.data)\n'
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/table/0")
        return render_template('login.html', message="Wrong login or password" + msg, form=form, up=False)
    return render_template('login.html', title='Авторизация', form=form, up=False)


@app.route('/send_param', methods=['GET', 'POST'])
@login_required
def send_param():
    form = Send_param()
    db_sess = db_session.create_session()
    param = db_sess.query(Status).filter(Status.token == current_user.token).first()
    # print(param)
    if request.method == 'GET':
        form.light_on.data = param.light_on
        form.heat_on.data = param.heat_on
        form.heat_off.data = param.heat_off
        form.pump_on.data = param.pump_on
    if form.validate_on_submit():
        if not (0 < form.light_on.data < 1024):
            return render_template('send_param.html', title='1Ошибка в отправке параметров', up=False, form=form,
                                   message="Укажите порог включения подсветки в пределах 0-1024")
        if not (0 < form.heat_on.data < 30) or not (0 < form.heat_off.data < 30):
            return render_template('send_param.html', title='2Ошибка в отправке параметров', up=False, form=form,
                                   message="Укажите температуру в пределах 0-30")
        if form.heat_on.data >= form.heat_off.data:
            return render_template('send_param.html', title='3Ошибка в отправке параметров', up=False, form=form,
                                   message="Температура включения должна быть ниже температуры выключения подогрева")
        if not (0 < form.pump_on.data < 1024):
            return render_template('send_param.html', title='4Ошибка в отправке параметров', up=False, form=form,
                                   message="Укажите порого включения полива в пределах 0-1024")
        db_sess = db_session.create_session()
        status = db_sess.query(Status).filter(Status.token == current_user.token).first()
        status.light_on = form.light_on.data
        status.heat_on = form.heat_on.data
        status.heat_off = form.heat_off.data
        status.pump_on = form.pump_on.data
        status.send = 0
        db_sess.commit()
        print('Ок')
        return redirect("/success")
    print('овторяем')
    return render_template('send_param.html', title='Передача параметров', form=form, up=False)

@app.route("/update/<token>")
def update(token):
    db_sess = db_session.create_session()
    status = db_sess.query(Status).filter(Status.token == token).first()
    data = {}
    data['light_on'] = status.light_on
    data['heat_on'] = status.heat_on
    data['heat_off'] = status.heat_off
    data['pump_on'] = status.pump_on
    data['pump'] = status.pump
    data['heat'] = status.heat
    data['led'] = status.led
    data['fan'] = status.fan
    status.send = 1
    db_sess.commit()
    print(data)
    return data

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return render_template('readme.html', up=False)

@app.route('/success')
def success():
    return render_template('success.html', up=False)

@app.route('/gauge')
def gauge():
    return render_template('gauge.html', up=False)

@app.route('/mygauge')
def mygauge():
    return render_template('my_gauge.html', up=False)

@app.route('/readme')
def readme():
    return render_template('readme.html', up=False)

@app.route('/dashboard')
@login_required
def dashboard():
    db_sess = db_session.create_session()
    base_data = db_sess.query(Sensors).filter(current_user.is_authenticated,
                                              (Sensors.token == current_user.token) | (current_user.id == 1)).all()
    # print(base_data)
    return render_template('dashboard.html', token=current_user.token, data=base_data[-1], up=True)


@app.route('/add_sensors')
def add_sensors():
    db_sess = db_session.create_session()
    sensor = Sensors()
    sensor.temp_in=request.args.get('t_in')
    sensor.humidity_in=request.args.get('h_in')
    sensor.temp_out=request.args.get('t_out')
    sensor.token = request.args.get('token')
    sensor.humidity_out=request.args.get('h_out')
    sensor.moisture1=request.args.get('mois1')
    sensor.moisture2 = request.args.get('mois1')
    sensor.light = request.args.get('light')
    sensor.pump = request.args.get('pump')
    sensor.heat = request.args.get('heat')
    sensor.led = request.args.get('led')
    sensor.fan = request.args.get('fan')

    # print(sensor)



    db_sess.add(sensor)
    db_sess.commit()
    return "OK"


    return render_template('success.html', up=False)


@app.route('/table/<page>')
@login_required
def table_page(page):
    db_sess = db_session.create_session()


    base_data = db_sess.query(Sensors).filter(current_user.is_authenticated, (Sensors.token == current_user.token) | (current_user.id == 1)).all()
    # print(base_data)
    users = db_sess.query(User).all()
    names = {name.token: (name.surname, name.name, name.email) for name in users}
    # print(int(len(base_data) / 10))
    return render_template('table.html', len_data=int(len(base_data) / 10) + 1,
                           names=names, base_data=base_data[::-1], page=int(page), token=current_user.token,
                           up=True)

@app.route('/grafik')
@login_required
def grafik():
    count = 12
    db_sess = db_session.create_session()
    base_data = db_sess.query(Sensors).filter(current_user.is_authenticated,
                                              (Sensors.token == current_user.token) | (current_user.id == 1)).all()
    # print(base_data)
    line_temp_in = []
    line_temp_out = []
    name_x = []
    humidity_in = []
    moisture1 = []

    for i in base_data[-count:]:
        #line_temp_in.append({'x':i.date.strftime("%H:%M:%S"), 'y':i.temp_in/1000 })
        #line_temp_out.append({'x':i.date.strftime("%H:%M:%S"), 'y':i.temp_out/1000 })
        line_temp_in.append(i.temp_in)
        line_temp_out.append(i.temp_out)
        name_x.append(i.date.strftime("%H%M"))
        humidity_in.append(i.humidity_in)
        moisture1.append(i.moisture1)
    # print(line_temp_in)
    # print(line_temp_out)
    return render_template('grafik.html', line1=line_temp_in, token=current_user.token, line2=humidity_in, line3=moisture1, name_x=name_x, name_grafik='График температуры', up=True )

@app.route("/update5")
def update5():
    level_led = ran.randint(0, 1000)
    level_fan = ran.randint(20, 30)
    level_head_up = ran.randint(0, 20)
    level_head_down = ran.randint(level_head_up, 30)
    level_hudrom = ran.randint(0, 1000)
    return f'<p>level_led={level_led}<p>level_fan={level_fan}<p>level_head_up={level_head_up}<p>level_head_down={level_head_down}<p>level_hudrom={level_hudrom}'

@app.route("/update_2")
def update_2():
    level_led = ran.randint(0, 1000)
    level_fan = ran.randint(20, 30)
    level_head_up = ran.randint(0, 20)
    level_head_down = ran.randint(level_head_up, 30)
    level_hudrom = ran.randint(0, 1000)
    return f'level_led={level_led}#level_fan={level_fan}#level_head_up={level_head_up}#level_head_down={level_head_down}#level_hudrom={level_hudrom}'

@app.route("/update_3")
def update_3():
    level_led = ran.randint(0, 1000)
    level_fan = ran.randint(20, 30)
    level_head_up = ran.randint(0, 20)
    level_head_down = ran.randint(level_head_up, 30)
    level_hudrom = ran.randint(0, 1000)
    return f'#_1{level_led}#_2{level_fan}#_3{level_head_up}#_4{level_head_down}#_5{level_hudrom}'



'''@app.route('/process_data/', methods=['POST'])
def doit():
    data = request.get_json(silent=True)
    index = data["index"]
    print(data, index)
    return data'''


@app.route('/process_data/', methods=['POST'])
def doit2():
    index = request.form['index']
    token = current_user.token
    print(index, token)
    return index
    # ... обработать данные ...


if __name__ == '__main__':

    app.run(port=5000, host='127.0.0.1')
    '''serve(app, host='127.0.0.1', port=5000)'''