from flask import request,Response
from datetime import datetime
from flaskr.common_method import db_setting, security
import json
# server=Flask(__name__)
def usermessage(app):
    @app.route('/userinfo',methods=['get'])
    def select_userinfo():#查看用户信息
        token = request.headers['access_token']  # 获取header里的token
        parse_token= security.parse_token(token)#解析token
        if (parse_token == 1):
            return {"code": 1, "message": "token已过期", "success": "false"}
        elif (parse_token == 2):
            return {"code": 2, "message": "token认证失败", "success": "false"}
        elif (parse_token == 3):
            return {"code": 3, "message": "非法的token", "success": "false"}
        else:
            # user_id=request.values.get('user_id')
            userid=(parse_token['data']['userid'])#查询用户id
            sql = "select * from (SELECT * from user_message where id='%s' ) AS a INNER JOIN (select avatar_image_url,user_id from user_avatar_image where user_id='%s' ORDER BY create_time DESC LIMIT 1)as b where a.id=b.user_id" % (userid,userid)
            res = db_setting.my_db(sql)
            tinydict = {'user_name': '', 'birthday': '', 'sex': '','hobby': '','province': '','city': '','self_description':'','user_avatar':''}
            tinydict['user_name'] = res[0][2]
            tinydict['sex'] = res[0][3]
            tinydict['birthday'] = res[0][4].strftime('%Y-%m-%d')
            tinydict['hobby'] = res[0][5]
            tinydict['province'] = res[0][6]
            tinydict['city'] = res[0][7]
            tinydict['self_description'] = res[0][8]
            tinydict['user_avatar'] = res[0][10]
            return {"code": 200, "message": "ok", "data": tinydict, "success": "true"}
            # return Response(json.dumps(tinydict,ensure_ascii=False),mimetype='application/json')

    @app.route('/update_userinfo', methods=['post'])
    def update_userinfo():  # 更改用户信息
        token = request.headers['access_token']  # 获取header里的token
        parse_token = security.parse_token(token)  # 解析token
        if (parse_token == 1):
            return {"code": 1, "message": "token已过期", "success": "false"}
        elif (parse_token == 2):
            return {"code": 2, "message": "token认证失败", "success": "false"}
        elif (parse_token == 3):
            return {"code": 3, "message": "非法的token", "success": "false"}
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
            return {"code": 200, "message": "更改用户信息成功",  "success": "true"}
            # return '更改用户信息成功'

