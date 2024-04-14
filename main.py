import datetime

from flask import Flask, render_template, request, redirect, jsonify
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
from data.config import name_base
from data.users import User
from data.sensors import Sensors
from data.login_form import LoginForm
from data.send_param import Send_param
from data.status import Status
from static.text.buttons_name import name_button
from flask_restful import reqparse, abort, Api, Resource


db_session.global_init(name_base)
app = Flask(__name__)
api = flask_restful.Api(app)






app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

def dev_status():
    db_sess = db_session.create_session()
    status = db_sess.query(Status).filter(Status.token == current_user.token).first()
    status_dev = {'sending': status.sending, 'date': status.date_down.strftime("%d.%m.%Y %H:%M:%S")}
    print('dev_status')
    print(status.pump, status.fan, status.heat, status.led, status.sending)

    if status.pump:
        status_dev['pump'] = 'Вкл'
    else:
        status_dev['pump'] = 'Выкл'
    if status.fan:
        status_dev['fan'] = 'Вкл'
    else:
        status_dev['fan'] = 'Выкл'
    if status.led:
        status_dev['led'] = 'Вкл'
    else:
        status_dev['led'] = 'Выкл'
    if status.heat:
        status_dev['heat'] = 'Вкл'
    else:
        status_dev['heat'] = 'Выкл'
    return status_dev


def correkt_date_time():
    dt = datetime.datetime.now()
    delta_time = datetime.timedelta(hours=3)
    dt += delta_time
    return dt

@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/1')
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
    print(f'send_param')
    form = Send_param()
    db_sess = db_session.create_session()
    param = db_sess.query(Status).filter(Status.token == current_user.token).first()
    # print(param)
    if request.method == 'GET':
        print(f'send_param GET')
        form.light_on.data = param.light_on
        form.heat_on.data = param.heat_on
        form.heat_off.data = param.heat_off
        form.pump_on.data = param.pump_on
        form.water.data = param.water
        form.delta_loop.data = param.delta_loop
        form.delta_send.data = param.delta_send
    if form.validate_on_submit():
        print(f'send_param POST')
        if not (0 < form.light_on.data < 100):
            return render_template('send_param.html', title='Ошибка в отправке параметров', up=False, form=form,
                                   message="Укажите порог включения подсветки в пределах 0-1024")
        if not (0 < form.heat_on.data < 30) or not (0 < form.heat_off.data < 30):
            return render_template('send_param.html', title='Ошибка в отправке параметров', up=False, form=form,
                                   message="Укажите температуру в пределах 0-30")
        if form.heat_on.data >= form.heat_off.data:
            return render_template('send_param.html', title='Ошибка в отправке параметров', up=False, form=form,
                                   message="Температура включения должна быть ниже температуры выключения подогрева")
        if not (0 < form.pump_on.data < 100):
            return render_template('send_param.html', title='Ошибка в отправке параметров', up=False, form=form,
                                   message="Укажите порого включения полива в пределах 0-1024")
        if not (0 < form.water.data < 100):
            return render_template('send_param.html', title='Ошибка в отправке параметров', up=False, form=form,
                                   message="Укажите порого включения воды в пределах 0-1024")
        if not (0 < form.delta_send.data < 100):
            return render_template('send_param.html', title='Ошибка в отправке параметров', up=False, form=form,
                                   message="Укажите время межды отправками в секундах в пределах 0-1024")
        if not (0 < form.delta_loop.data < 100):
            return render_template('send_param.html', title='Ошибка в отправке параметров', up=False, form=form,
                                   message="Укажите время межды отправками в секундах в пределах 0-1024")
        db_sess = db_session.create_session()
        status = db_sess.query(Status).filter(Status.token == current_user.token).first()
        status.light_on = form.light_on.data
        status.heat_on = form.heat_on.data
        status.heat_off = form.heat_off.data
        status.pump_on = form.pump_on.data
        status.sending = 0
        status.water = form.water.data
        status.delta_send = form.delta_send.data
        status.delta_loop = form.delta_loop.data
        status.date_up = correkt_date_time()
        db_sess.commit()




        print('Ок')
        return redirect("/send_param")
    print('Повторяем')
    return render_template('send_param.html', title='Передача параметров', status=dev_status(), text_button=name_button, form=form, up=False)

@app.route("/update/<token>")
def update(token):
    print(f'update/{token}')
    db_sess = db_session.create_session()
    status = db_sess.query(Status).filter(Status.token == token).first()
    status.sending = 1
    data = {}
    data['light_on'] = status.light_on
    data['heat_on'] = status.heat_on
    data['heat_off'] = status.heat_off
    data['pump_on'] = status.pump_on
    data['pump'] = status.pump
    data['heat'] = status.heat
    data['led'] = status.led
    data['fan'] = status.fan
    data['water'] = status.water
    data['control'] = status.control
    data['delta_send'] = status.delta_send
    data['delta_loop'] = status.delta_loop
    status.date_down = correkt_date_time()
    # print(status.date_up, type(status.date_up))
    # print(status.date_down, type(status.date_down))
    delta = status.date_down - status.date_up
    # print(delta.total_seconds())
    data['sending'] = int(delta.total_seconds())
    db_sess.commit()
    print(data, correkt_date_time())
    return data

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return render_template('readme.html',status=dev_status(), up=False)

@app.route('/success')
def success():
    return render_template('success.html',status=dev_status(), up=False)

@app.route('/gauge')
def gauge():
    return render_template('gauge.html',status=dev_status(), up=False)

@app.route('/mygauge')
def mygauge():
    return render_template('my_gauge.html',status=dev_status(), up=False)

@app.route('/readme')
def readme():
    return render_template('readme.html',status=dev_status(), up=False)

@app.route('/')
@app.route('/dashboard')
@login_required
def dashboard():
    db_sess = db_session.create_session()
    status = db_sess.query(Status).filter(Status.token == current_user.token).first()
    base_data = db_sess.query(Sensors).filter(current_user.is_authenticated, (Sensors.token == current_user.token)
                                              | (current_user.id == 1)).all()
    # print(base_data)
    return render_template('dashboard.html', status=dev_status(), token=current_user.token, data=base_data[-1], text_button=name_button, up=False)


@app.route('/add_sensors')
def add_sensors():
    db_sess = db_session.create_session()
    sensor = Sensors()
    sensor.date = correkt_date_time()
    sensor.temp_in = request.args.get('t_in')
    sensor.humidity_in = request.args.get('h_in')
    sensor.temp_out = request.args.get('t_out')
    sensor.token = request.args.get('token')
    sensor.humidity_out = request.args.get('h_out')
    sensor.moisture1 = request.args.get('mois1')
    sensor.moisture2 = request.args.get('mois1')
    sensor.light = request.args.get('light')
    sensor.pump = request.args.get('pump')
    sensor.heat = request.args.get('heat')
    sensor.led = request.args.get('led')
    sensor.fan = request.args.get('fan')
    sensor.water = request.args.get('water')
    # print(sensor)



    db_sess.add(sensor)
    db_sess.commit()
    return "OK"


    return render_template('success.html', up=False)


@app.route('/table/<page>')
@login_required
def table_page(page):
    db_sess = db_session.create_session()
    print('table', correkt_date_time())

    base_data = db_sess.query(Sensors).filter(current_user.is_authenticated, (Sensors.token == current_user.token) | (current_user.id == 1)).all()
    # print(base_data)
    users = db_sess.query(User).all()
    names = {name.token: (name.surname, name.name, name.email) for name in users}
    # print(int(len(base_data) / 10))
    return render_template('table.html', len_data=int(len(base_data) / 10) + 1,
                           names=names, status=dev_status(), text_button=name_button, base_data=base_data[::-1], page=int(page), token=current_user.token,
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
    return render_template('grafik.html',status=dev_status(), text_button=name_button, line1=line_temp_in, token=current_user.token, line2=humidity_in, line3=moisture1, name_x=name_x, name_grafik='График температуры', up=True )

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


@app.route('/buttons', methods=['GET', 'POST'])
def buttons():
    db_sess = db_session.create_session()
    status = db_sess.query(Status).filter(Status.token == current_user.token).first()
    if request.is_json:
        print(status.sending)
        text = request.args.get('button_text')
        id = request.args.get('name')
        status.sending = 0
        status.date_up = correkt_date_time()
        if id == 'pump':
            status.pump = not status.pump
            on_off = 'Вкл' if status.pump else 'Выкл'
        if id == 'fan':
            status.fan = not status.fan
            on_off = 'Вкл' if status.fan else 'Выкл'
        if id == 'heat':
            status.heat = not status.heat
            on_off = 'Вкл' if status.heat else 'Выкл'
        if id == 'led':
            status.led = not status.led
            on_off = 'Вкл' if status.led else 'Выкл'
        db_sess.commit()
        print(on_off, status.sending, status.date_up)
        return jsonify({'html_paste': on_off})


# ... обработать данные ...


if __name__ == '__main__':

    app.run(port=5000, host='127.0.0.1')
    '''serve(app, host='127.0.0.1', port=5000)'''
