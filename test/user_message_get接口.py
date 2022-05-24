from flask import Flask,request
from flaskr import db
import json
# from gevent import pywsgi
server=Flask(__name__)
sql='SELECT * from user_message '
@server.route('/login',methods=['get'])
def login():
    res=db.my_db(sql)
    if res:
        tinydict={'Name': '', 'Age': '', 'sex': ''}
        tinydict['Name']=res[0][1]
        tinydict['Age'] = res[0][3].strftime('%Y-%m-%d')
        tinydict['sex'] = res[0][2]
    return json.dumps(tinydict,ensure_ascii=False,indent=4)
server.run(host='127.0.0.1',port=8998,debug=True)

