from data.sensors import Sensors
from flask import Flask
from data import db_session
from data.users import User
from random import randint, choice

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
# Первая работа

def main():
    db_session.global_init("db/teplica.db")
    session = db_session.create_session()

    sensor = Sensors()
    sensor.token = choice(
        ['sTGANTFwpHVLMXz', 'mQXWEudnskQgwHk', 'aDnbGUhmkyrByvH', 'BnAdfWKwsdDpFFp', 'bXgLsghZdNVDUDM'])

    sensor.temp_in = randint(0,30)
    sensor.humidity_in = randint(0, 100)
    sensor.temp_out = randint(0, 30)
    sensor.humidity_out = randint(0, 100)
    sensor.moisture1 = randint(0, 1023)
    sensor.moisture2 = randint(0, 1023)
    sensor.light = randint(0, 1023)
    sensor.pump = randint(0, 1)
    sensor.heat = randint(0, 1)
    sensor.led = randint(0, 1)
    sensor.fan = randint(0, 1)


    session.add(sensor)


    session.commit()


if __name__ == '__main__':
    main()