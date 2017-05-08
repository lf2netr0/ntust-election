# -*- coding: UTF-8 -*-
import logging
import json
import falcon
from helper.helper import error_response, encrypt, success_response, hasher
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy import create_engine, schema

from database.mail_tosend import mail_tosend
from database.elector import Elector as elector
from database.prepared_token import Prepared_Token as prepared_token
from database.token import Token as token
from database.connector import dbconnect
from database.base import Base


engine = dbconnect()

Session = sessionmaker()
Session.configure(bind=engine)
session = Session()

class APIResource:
    def on_get(self, req, resp):
        resp.body = json.dumps({
            'message': 'Hello'
        })

class Elector:
    def on_get(self, req, resp):
        from config import config
        id_type = req.params['type']
        value = req.params['value']
        project_id = req.params['project_id']
        if id_type == '2':
            elector_data = session.query(elector
                ).filter(elector.student_id == value, elector.project_id == project_id
                ).first()
        elif id_type == '1':
            elector_data = session.query(elector
                ).filter(elector.card_id==hasher(value), elector.project_id == project_id
                ).first()


        if elector_data == None:
            message = error_response("查無此卡號/學號")
        else:
            student_data = {
                'student_id': elector_data.student_id,
                'name': elector_data.name,
                'department': elector_data.department
            }
            message = success_response(student_data)

        resp.body = message

class Token:
    def on_post(self, req, resp):
        import datetime
        from config import config
        id_type = req.params['type']
        value = req.params['value']
        project_id = req.params['project_id']

        if id_type == '2':
            elector_data = session.query(elector.student_id,elector.status
                ).filter(elector.student_id == value, elector.project_id == project_id
                ).first()
        elif id_type == '1':
            elector_data = session.query(elector.student_id,elector.status
                ).filter(elector.card_id == hasher(value), elector.project_id == project_id
                ).first()
                
        if elector_data == None:
            message = error_response("查無此卡號/學號")
        else:
            if elector_data[1] == 1:
                message = error_response("該學生授權碼已被取用")
            else:
                tmp = session.query(prepared_token.token, prepared_token.id
                    ).filter(prepared_token.project_id == project_id
                    ).first()
                taketoken = tmp[0]
                t_id = tmp[1]

                session.query(elector
                    ).filter(elector.student_id == elector_data.student_id, elector.project_id == project_id
                    ).update({'status':1,}, synchronize_session=False)
                session.query(prepared_token
                    ).filter(prepared_token.id == t_id
                    ).delete(synchronize_session=False)

                encrypted_id = encrypt(elector_data.student_id, config['public_keys'])

                session.add(token(
                    token = taketoken,
                    owner = encrypted_id,
                    project_id = project_id,
                    used = False
                ))

                session.add(mail_tosend(
                    student_id = elector_data.student_id,
                    gettime = datetime.datetime.now()
                ))
                session.commit()
                message = success_response(taketoken)

        resp.body = message

    def on_delete(self, req, resp):
        token_record = ()
        usedtoken = req.params['token']
        project_id = req.params['project_id']

        token_record = session.query(token.used
            ).filter(token.token == usedtoken , token.project_id == project_id
            ).first()
        if token_record != None:
            session.query(token
                ).filter(token.token == usedtoken, token.project_id == project_id
                ).update({'used':1,}, synchronize_session=False)
            session.commit()

            message = success_response("success change")

        else:
            message =  error_response('查無此授權碼')

        resp.body = message


class Verify:
    def on_get(self, req, resp):
        gettoken = req.params['token']
        project_id = req.params['project_id']

        used = session.query(token.used
            ).filter(token.token == gettoken, token.project_id == project_id
            ).first()

        if used != None:
            message = success_response(not used[0])
        else:
            message =  error_response('查無此授權碼')
        resp.body = message

class Middleware:
    def process_response(self, req, resp, resource):
        session.close()
        engine.dispose()

api = falcon.API(middleware=[Middleware()])

api.add_route('/', APIResource())
api.add_route('/token', Token())
api.add_route('/verify', Verify())
api.add_route('/elector', Elector())