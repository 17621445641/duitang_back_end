from flask import Flask,request
from flaskr import db
import json
def tt(server):
    sql = 'SELECT * from user_message '
    @server.route('/login',methods=['post'])

# server=Flask(__name__)

# @server.route('/login',methods=['post'])
    def login():
        user_name=request.json.get('account')
        sex = request.json.get('password')
        # token=request.headers['access_token']#获取header里的token
        if(user_name=="测试用户" and sex=='男'):
            res=db.my_db(sql)
            tinydict = {'Name': '', 'Age': '', 'sex': ''}
            tinydict['Name']=res[0][1]
            tinydict['Age'] = res[0][3].strftime('%Y-%m-%d')
            tinydict['sex'] = res[0][2]
            return json.dumps(tinydict, ensure_ascii=False, indent=4)
        else:
            message="用户有误3"
            # return json.dumps(message, ensure_ascii=False, indent=4)
            return message
    # server.run(host='127.0.0.1',port=8998,debug=True)

