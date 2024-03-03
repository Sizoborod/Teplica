import datetime
import random
from random import randint, choice
import schedule
import requests

params = {'t_in': 10, 'h_in': 66, 't_out': 8, 'h_out': 47, 'mois1': 654, 'mois2': 330, 'light': 491, 'pump': 0, 'heat': 1, 'led': 1, 'fan': 1}
def job():
    temp= random.randint(0,100)
    hudr = random.randint(0, 100)
    request = (f"https://script.google.com/macros/s/AKfycbxEGjW__Vir_EeWNA-bpMZORag_khkWjwkv4FQaoozD5E-"
               f"LYgKFKB4vZ8NKqcDMSGPdBA/exec?temperature={temp}&humidity={hudr}")
    response = requests.get(request)
    print(datetime.datetime.now())
    print("Http статус:", response.status_code, "(", response.reason, ")")

def sensors():
    global params
    params['token'] = choice(['sTGANTFwpHVLMXz','mQXWEudnskQgwHk', 'aDnbGUhmkyrByvH', 'BnAdfWKwsdDpFFp', 'bXgLsghZdNVDUDM'])
    params['t_in'] += randint(0, 6) - 3
    params['h_in'] += randint(0, 10) - 5
    params['t_out'] += randint(0, 6) - 3
    params['h_out'] += randint(0, 10) - 5
    params['mois1'] += randint(0, 100) - 50
    params['mois2'] += randint(0, 100) - 50
    params['light'] += randint(0, 100) - 50
    params['pump'] = randint(0, 1)
    params['heat'] = randint(0, 1)
    params['led'] = randint(0, 1)
    params['fan'] = randint(0, 1)
    #http://127.0.0.1:5000/add_sensors?t_in=55&h_in=88&t_out=55&h_out=88&mois1=444&mois2=555&light=258&pump=1&heat=0&led=0&fan=1
    request = (f"http://127.0.0.1:5000/add_sensors?")
    response = requests.get(request, params=params)
    print(datetime.datetime.now(), params)
    print("Http статус:", response.status_code, "(", response.reason, ")")


schedule.every().minute.at(":00").do(sensors)

while True:
    schedule.run_pending()