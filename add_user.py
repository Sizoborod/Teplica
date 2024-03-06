
from flask import Flask
from data import db_session
from data.users import User

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

# Добавляем капитана
def main():
    db_session.global_init("db/teplica.db")
    session = db_session.create_session()

    user = User()
    user.surname = "Scott"
    user.name = "Ridley"
    user.email = "cap@cap.ru"
    user.hashed_password = "cap"
    user.set_password(user.hashed_password)
    user.token =
    session.add(user)

    session.commit()
    user = User()
    user.surname = "Степанова"
    user.name = "Аделина"
    user.email = "ds1@cap.ru"
    user.hashed_password = "ds1"
    user.set_password(user.hashed_password)
    user.token = "mQXWEudnskQgwHk"
    session.add(user)

    session.commit()
    user = User()
    user.surname = "Никитина"
    user.name = "Надежда"
    user.email = "ds6@cap.ru"
    user.hashed_password = "ds6"
    user.set_password(user.hashed_password)
    user.token = "aDnbGUhmkyrByvH"
    session.add(user)


    session.commit()
    user = User()
    user.surname = "Капралова"
    user.name = "Нина"
    user.email = "ds5@cap.ru"
    user.hashed_password = "ds5"
    user.set_password(user.hashed_password)
    user.token = "BnAdfWKwsdDpFFp"
    session.add(user)

    session.commit()
    user = User()
    user.surname = "Васильева"
    user.name = "Надежда"
    user.email = "ds4@cap.ru"
    user.hashed_password = "ds4"
    user.set_password(user.hashed_password)
    user.token = "bXgLsghZdNVDUDM"
    session.add(user)
    session.commit()


if __name__ == '__main__':
    main()