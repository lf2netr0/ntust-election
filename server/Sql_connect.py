import mysql.connector
import json
import ast
import datetime
import time
import function
from config import config
gtk = function.token()
class sql:
    def __init__(self):
        self.cnx = mysql.connector.connect(**config)
        self.cursor = self.cnx.cursor(buffered = True)
        self.cursor.execute('set names utf8')
    
    def prepare_token_catch(self):
        query_catch=('Select min(id),token from token_prepare where enabled = 0 ;')
        self.cursor.execute(query_catch)
        data = self.cursor.fetchall()
        query_enabled=('update token_prepare set enabled = 1 where id ='+str(data[0][0])+';')
        self.cursor.execute(query_enabled)
        return data[0][1]

    def prepare_token_insert(self,p_token):
        for i in range(0,len(p_token)):
            add_prepare = ("INSERT INTO token_prepare "
                          "(token,enabled) "
                          "VALUES (%(token)s,%(enabled)s);")
            data_prepare = {
                'token': p_token[i],
                'enabled': '0'
            }
            self.cursor.execute(add_prepare, data_prepare)
        self.cnx.commit()

    def token_search(self,req):

        token = []#store new token from database
        #identify the id_type
        if req['id_type'] == '2':
            id_type='card_id'
        elif req['id_type'] == '1':
            id_type = 'id'
        query_s = ('Select id from Student where ' + id_type + "='" + req['id'] + "';")
        self.cursor.execute(query_s)
        data = self.cursor.fetchall()

        if data == []:#no data in server
            ts = time.time()
            st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
            result = {
                'status': 'error_001',
                'data': 'no_id',
                'timestamp': st
            }#mistake return
            return  result
        else:
            ts = datetime.datetime.now().strftime("%H:%M:%S")#get timestamp

            #------------generate token and insert to database------------#
            query_s = ('Select solgan from Election where id=' + req['election_id'] + ';')
            self.cursor.execute(query_s)
            solgan = self.cursor.fetchone()
            add_token = ("INSERT INTO Token "
                          "(token,election_id,student_id,enabled) "
                          "VALUES (%(token)s, %(election_id)s, %(student_id)s, %(enabled)s);")
            data_token = {
                'token': solgan[0] + self.prepare_token_catch(),
                'election_id': req['election_id'],
                'student_id': data[0][0],
                'enabled': 1
            }
            token.append(data_token['token'])#new token save in list
            self.cursor.execute(add_token, data_token)
            #---------------------------------------------------------------------------------#
            self.cnx.commit()

            self.cursor.close()
            self.cnx.close()

            token_result = {
                'status': 'success',
                'data': {
                    'token': token
                },
                'timestamp': ts
            }
            return token_result

#sql().prepare_token_insert(gtk.init_prepare_token())
