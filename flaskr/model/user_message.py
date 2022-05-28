from flask import request
from flask import Response
from datetime import datetime
from flaskr.common_method import db_setting, security
import json
# server=Flask(__name__)
def usermessage(app):
    @app.route('/userinfo',methods=['get'])
    def select_userinfo():#查看用户信息
        token = request.headers['access_token']  # 获取header里的token
        parse_token= security.parse_token(token)#解析token
        if(parse_token==1 ):
            return 'token已过期'
        elif(parse_token==2):
            return 'token认证失败'
        elif (parse_token == 3):
            return '非法的token'
        else:
            # user_id=request.values.get('user_id')
            userid=(parse_token['data']['userid'])#查询用户id
            sql = "SELECT * from user_message where id='%s' " % (userid)
            res = db_setting.my_db(sql)
            tinydict = {'user_name': '', 'birthday': '', 'sex': '','hobby': '','province': '','city': '','self_description':''}
            tinydict['user_name'] = res[0][2]
            tinydict['sex'] = res[0][3]
            tinydict['birthday'] = res[0][4].strftime('%Y-%m-%d')
            tinydict['hobby'] = res[0][5]
            tinydict['province'] = res[0][6]
            tinydict['city'] = res[0][7]
            tinydict['self_description'] = res[0][8]
            return Response(json.dumps(tinydict,ensure_ascii=False),mimetype='application/json')

    @app.route('/update_userinfo', methods=['post'])
    def update_userinfo():  # 更改用户信息
        token = request.headers['access_token']  # 获取header里的token
        parse_token = security.parse_token(token)  # 解析token
        if (parse_token == 1):
            return 'token已过期'
        elif (parse_token == 2):
            return 'token认证失败'
        elif (parse_token == 3):
            return '非法的token'
        else:
            userid = (parse_token['data']['userid'])  # 查询用户id
            user_name = request.json.get('user_name')
            sex = request.json.get('sex')
            birthday = request.json.get('birthday')
            hobby = request.json.get('hobby')
            province = request.json.get('province')
            city = request.json.get('city')
            self_description = request.json.get('self_description')
            update_time = datetime.utcnow()
            sql = "UPDATE user_message SET `name` = '%s', `sex` = '%s', `birth_day` = '%s', `hobby` = '%s', `province` = '%s', `city` = '%s', `self_description` = '%s', `update_time` = '%s' WHERE `id` = '%s';" % (user_name,sex,birthday,hobby,province,city,self_description,update_time,userid)
            db_setting.my_db(sql)
            return '更改用户信息成功'

