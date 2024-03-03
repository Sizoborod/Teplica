import datetime
import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Sensors(SqlAlchemyBase):
    __tablename__ = 'sensors'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    temp_in = sqlalchemy.Column(sqlalchemy.Integer, nullable=True, default=0)
    humidity_in = sqlalchemy.Column(sqlalchemy.Integer, nullable=True, default=0)
    temp_out = sqlalchemy.Column(sqlalchemy.Integer, nullable=True, default=0)
    humidity_out = sqlalchemy.Column(sqlalchemy.Integer, nullable=True, default=0)
    moisture1 = sqlalchemy.Column(sqlalchemy.Integer, nullable=True, default=0)
    moisture2 = sqlalchemy.Column(sqlalchemy.Integer, nullable=True, default=0)
    light = sqlalchemy.Column(sqlalchemy.Integer, nullable=True, default=0)
    token = sqlalchemy.Column(sqlalchemy.String, nullable=True, default='NNNNNNNNNNN')
    pump = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    heat = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    led = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    fan = sqlalchemy.Column(sqlalchemy.Integer, default=0)


    def __repr__(self):
        return (f'<Sensors> {self.token}\n'
                f'temp_in = {self.temp_in} => humidity_in = {self.humidity_in}\n'
                f'temp_out = {self.temp_out} => humidity_out = {self.humidity_out}\n'
                f'moisture1 = {self.moisture1} => moisture2 = {self.moisture2}\n'
                f'light = {self.light}\n'
                f'pump\t=> \theat\t=> \tled\t=> \tfan\n'
                f'{self.pump}\t\t=> \t{self.heat}\t\t=> \t{self.led}\t=> \t{self.fan}\n')

