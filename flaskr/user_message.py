from flask import request
import security
import db_setting
from flaskr import db
import json
# server=Flask(__name__)
def usermessage(app):
    @app.route('/userinfo',methods=['get'])
    def select_userinfo():#查看用户信息
        token = request.headers['access_token']  # 获取header里的token
        parse_token=security.parse_token(token)#解析token
        if(parse_token==1 or parse_token==2 or parse_token==3 ):
            return 'token已过期'
        elif(parse_token==2):
            return 'token认证失败'
        elif (parse_token == 3):
            return '非法的token'
        else:
            userid=(parse_token['data']['userid'])#查询用户id
            sql = "SELECT * from user_message where id='%s' " % (userid)
            res = db_setting.my_db(sql)
            tinydict = {'Name': '', 'Age': '', 'sex': ''}
            tinydict['Name'] = res[0][1]
            tinydict['sex'] = res[0][2]
            tinydict['Age'] = res[0][3].strftime('%Y-%m-%d')
            return json.dumps(tinydict, ensure_ascii=False, indent=4)
