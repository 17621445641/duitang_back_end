from flask import request,Response
from datetime import datetime
from flaskr.common_method import db_setting, security,list_method,splicing_list
import requests
import json
def article_like(app):
    @app.route('/article_like', methods=['post'])
    def article_like():  # 文章喜欢和取消喜欢
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
            article_id = request.json.get('article_id')  # 文章id
            status = request.json.get('status')  # 根据status执行喜欢或者取消喜欢
            if (article_id):  # 判断是否传了article_id字段
                sql = "select id from article where id='%s'" % (article_id)
                if (db_setting.my_db(sql)):  # 查询是否含有此文章id
                    sql2 = "select click_status from article_click where user_id='%s'and article_id='%s'" % (userid,article_id)#查询数据库表中是否有记录
                    if(status==0): #判断为0的时候执行取消喜欢
                        if (db_setting.my_db(sql2) and db_setting.my_db(sql2)[0][0] == 1):  # 查询是否用户已点赞，未有记录则插入一条点赞记录,已有记录且状态为未点赞，则进行点赞
                            update_time = datetime.utcnow()
                            sql3 = "UPDATE article_click SET click_status=0,update_time = '%s' WHERE user_id = '%s' and article_id='%s'" % (
                            update_time, userid,article_id)
                            db_setting.my_db(sql3)
                            return {"code": 200, "message": "取消喜欢成功","success":"true"}
                        elif(db_setting.my_db(sql2) and db_setting.my_db(sql2)[0][0] == 0):
                            return {"code": 500, "message": "已取消喜欢,无法再取消喜欢","success":"false"}
                        else:
                            return {"code": 500, "message": "取消喜欢失败,未找到记录","success":"false"}
                    elif(status==1):#判断为1的时候执行喜欢
                        if (db_setting.my_db(sql2) and db_setting.my_db(sql2)[0][0] == 0):
                            update_time = datetime.utcnow()
                            sql3 = "UPDATE article_click SET click_status=1,update_time = '%s' WHERE user_id = '%s' and article_id='%s'" % (
                                update_time, userid,article_id)
                            db_setting.my_db(sql3)
                            return {"code": 200, "message": "更新喜欢成功","success":"true"}
                        elif(db_setting.my_db(sql2) and db_setting.my_db(sql2)[0][0] == 1):
                            return {"code": 500, "message": "喜欢失败，已喜欢","success":"false"}
                        else:
                            create_time = datetime.utcnow()
                            sql4 = "INSERT INTO article_click (user_id, article_id, click_status, create_time, update_time) VALUES ( '%s', '%s', '%s', '%s', '%s')" % (
                            userid, article_id, 1, create_time, create_time)
                            db_setting.my_db(sql4)
                            return {"code": 200, "message": "新增喜欢成功","success":"true"}
                    else:
                        return {"code": 500, "message": "请输入正确的状态码(0取消喜欢，1喜欢)","success":"false"}
                else:
                    return {"code": 500, "message": "不存在的文章","success":"false"}
            else:
                return {"code": 500, "message": 'article_id字段不能为空',"success":"false"}

    @app.route('/click_list', methods=['get'])
    def click_list():  # 查询用户喜欢列表
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
            sql = "select  a.user_id,b.id,b.article_title,author_id,article_content,view_status,b.create_time as article_createtime,a.update_time as click_time from article_click as a INNER JOIN article as b on a.article_id=b.id and a.user_id='%s' and a.click_status=1 and article_id not in(select article_id from article_click as a INNER JOIN article as b on a.article_id=b.id and user_id!=author_id and view_status=0 and user_id='%s')ORDER BY click_time DESC" % (
                userid,userid)
            dict = {'user_id': '', 'article_id': '', 'article_title': '', 'author_id': '', 'article_content': '',
                    'view_status': '', 'article_create_time': '','click_time':''}
            click_list = list_method.list_method(sql, dict)
            resp=[]
            for num in click_list:
                for i in num.keys():
                    if(i=='author_id'):
                        url='http://127.0.0.1:8998/get_avatar'
                        params={'user_id': num[i]}
                        headers={'access_token':token}
                        data_m=requests.get(url=url,params=params,headers=headers)
                        resp.append(data_m.json()['data'])
            last_list=splicing_list.splicing_list(click_list,resp)
            # print(last_list)
            return {"code": 200, "message": "ok","data":last_list,"success":"true"}
        # return Response(json.dumps(like_list, ensure_ascii=False), mimetype='application/json')#返回json串