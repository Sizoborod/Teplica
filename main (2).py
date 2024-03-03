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
from data.login_form import LoginForm
from data.sensors import Sensors


from flask_restful import reqparse, abort, Api, Resource



app = Flask(__name__)
api = flask_restful.Api(app)

app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/')
def main_window():
    return render_template('object_manager.html')

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
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/table")
        return render_template('login.html', message="Wrong login or password", form=form)
    return render_template('login.html', title='Authorization', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/table")

@app.route('/success')
def success():
    return render_template('success.html')


@app.route('/add_sensors')
def add_sensors():
    db_sess = db_session.create_session()
    sensor = Sensors()
    sensor.temp_in=request.args.get('t_in')
    sensor.humidity_in=request.args.get('h_in')
    sensor.temp_out=request.args.get('t_out')
    sensor.humidity_out=request.args.get('h_out')
    sensor.moisture1=request.args.get('mois1')
    sensor.moisture2 = request.args.get('mois1')
    sensor.light = request.args.get('light')
    sensor.pump = request.args.get('pump')
    sensor.heat = request.args.get('heat')
    sensor.led = request.args.get('led')
    sensor.fan = request.args.get('fan')

    print(sensor)



    db_sess.add(sensor)
    db_sess.commit()
    return "OK"


    return render_template('success.html')


@app.route('/table/<page>')
def table_page(page):
    db_sess = db_session.create_session()
    base_data = db_sess.query(Sensors).all()
    print(int(len(base_data) / 10))
    return render_template('table.html',len_data=int(len(base_data) / 10) + 1, base_data=base_data[::-1], page=int(page))
@app.route('/grafik')
def grafik():
    count = 12
    db_sess = db_session.create_session()
    base_data = db_sess.query(Sensors).all()
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
    print(line_temp_in)
    print(line_temp_out)
    return render_template('grafik.html', line1=line_temp_in, line2=humidity_in, line3=moisture1, name_x=name_x, name_grafik='График температуры' )

@app.route("/update")
def update():
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

@app.route("/update_1")
def update_1():
    data = {}
    data['level_led'] = ran.randint(0, 1000)
    data['level_fan'] = ran.randint(20, 30)
    data['level_head_up'] = ran.randint(0, 20)
    data['level_head_down'] = ran.randint(data['level_head_up'], 30)
    data['level_hudrom'] = ran.randint(0, 1000)
    return data

if __name__ == '__main__':
    db_session.global_init("db/teplica.db")
    app.run(port=5000, host='127.0.0.1')
    '''serve(app, host='127.0.0.1', port=5000)'''