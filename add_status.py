from data.sensors import Sensors
from flask import Flask
from data import db_session
from data.status import Status
from random import randint, choice

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
# Первая работа

def main():
    db_session.global_init("db/teplica.db")
    session = db_session.create_session()

    status = Status()
    status.token = 'sTGANTFwpHVLMXz'

    status.light_on = randint(0,1024)
    status.heat_on = randint(0, 20)
    status.heat_off = randint(20, 30)
    status.pump_on = randint(0, 1024)
    status.pump = randint(0, 1)
    status.heat = randint(0, 1)
    status.led = randint(0, 1)
    status.fan = randint(0, 1)
    status.send = 0
    session.add(status)
    session.commit()
    status = Status()
    status.token = 'mQXWEudnskQgwHk'

    status.light_on = randint(0, 1024)
    status.heat_on = randint(0, 20)
    status.heat_off = randint(20, 30)
    status.pump_on = randint(0, 1024)
    status.pump = randint(0, 1)
    status.heat = randint(0, 1)
    status.led = randint(0, 1)
    status.fan = randint(0, 1)
    status.send = 0
    session.add(status)
    session.commit()
    status = Status()
    status.token = 'aDnbGUhmkyrByvH'

    status.light_on = randint(0, 1024)
    status.heat_on = randint(0, 20)
    status.heat_off = randint(20, 30)
    status.pump_on = randint(0, 1024)
    status.pump = randint(0, 1)
    status.heat = randint(0, 1)
    status.led = randint(0, 1)
    status.fan = randint(0, 1)
    status.send = 0
    session.add(status)
    session.commit()
    status = Status()
    status.token ='BnAdfWKwsdDpFFp'

    status.light_on = randint(0, 1024)
    status.heat_on = randint(0, 20)
    status.heat_off = randint(20, 30)
    status.pump_on = randint(0, 1024)
    status.pump = randint(0, 1)
    status.heat = randint(0, 1)
    status.led = randint(0, 1)
    status.fan = randint(0, 1)
    status.send = 0
    session.add(status)
    session.commit()
    status = Status()
    status.token = 'bXgLsghZdNVDUDM'
    status.light_on = randint(0, 1024)
    status.heat_on = randint(0, 20)
    status.heat_off = randint(20, 30)
    status.pump_on = randint(0, 1024)
    status.pump = randint(0, 1)
    status.heat = randint(0, 1)
    status.led = randint(0, 1)
    status.fan = randint(0, 1)
    status.send = 0
    session.add(status)
    session.commit()

if __name__ == '__main__':
    main()