import datetime
import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Status(SqlAlchemyBase):
    __tablename__ = 'status'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    date_up = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    date_down = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    token = sqlalchemy.Column(sqlalchemy.String, nullable=True, default='NNNNNNNNNNN')
    light_on = sqlalchemy.Column(sqlalchemy.Integer, nullable=True, default=0)
    heat_on = sqlalchemy.Column(sqlalchemy.Integer, nullable=True, default=0)
    heat_off = sqlalchemy.Column(sqlalchemy.Integer, nullable=True, default=0)
    pump_on = sqlalchemy.Column(sqlalchemy.Integer, nullable=True, default=0)
    pump = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    heat = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    led = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    fan = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    send = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    water = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    mode = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    delta_loop = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    delta_send = sqlalchemy.Column(sqlalchemy.Integer, default=0)

    def __repr__(self):
        return (f'<Status> {self.token}\n'
                f'date = {self.date} => light_on = {self.light_on}\n'
                f'heat_on = {self.heat_on} => heat_off = {self.heat_off}\n'
                f'pump_on = {self.heat_on} =>\n'
                f'pump\t=> \theat\t=> \tled\t=> \tfan\n'
                f'{self.pump}\t\t=> \t{self.heat}\t\t=> \t{self.led}\t=> \t{self.fan}\n')

