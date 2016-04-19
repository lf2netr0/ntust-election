import mysql.connector
import json
import ast
import datetime
import time
import function
from config import get_config
gtk=function.token()
class sql:

    def token_search(self,req):

        token=[]#store new token from database
        
        cnx = mysql.connector.connect(**get_config())
        cursor = cnx.cursor(buffered = True)
        cursor.execute('set names utf8')
        #identify the id_type
        if req[u'id_type'] =='2':
            id_type='card_id'
        elif req[u'id_type']=='1':
            id_type='id'
        query_s =('Select id from Student where '+id_type+"='"+req[u'id']+"';")
        cursor.execute(query_s)
        data = cursor.fetchall()

        if data==[]:#no data in server
            ts=time.time()
            st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
            result={'status':'error_001','data':'no_id','timestamp':st}#mistake return
            return  result
        else:
            ts=datetime.datetime.now().strftime("%H:%M:%S")#get timestamp

            #------------generate token and insert to database------------#
            query_s=('Select solgan from Election where id='+req[u'election_id']+';')
            cursor.execute(query_s)
            solgan=cursor.fetchone()
            add_token = ("INSERT INTO Token "
                          "(token,election_id,student_id,gettoken_time,enabled) "
                          "VALUES (%(token)s, %(election_id)s, %(student_id)s, %(gettoken_time)s,%(enabled)s);")
            data_token={
                'token':solgan[0]+gtk.generate_token(),
                'election_id':req[u'election_id'],
                'student_id':data[0][0],
                'gettoken_time':ts,
                'enabled':1
            }
            token.append(data_token['token'])#new token save in list
            cursor.execute(add_token, data_token)
            #---------------------------------------------------------------------------------#
            cnx.commit()
            cursor.close()
            cnx.close()
            token_result={'status':'success','data':{'token':token},'timestamp':ts}
            return token_result

