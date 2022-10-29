import decimal
from flask import request,Response
from datetime import datetime
import json
import requests
from flaskr.common_method import db_setting,security,list_method,splicing_list


def article_views(app):
    @app.route('/article_views', methods=['get'])
    def article_views():#浏览记录新增接口
            article_id = request.values.get('article_id')  # 文章id
            user_id = request.values.get('user_id')  # 文章id
            if (article_id):  # 判断是否传了article_id字段
                sql = "select id from article where id='%s'" % (article_id)
                if (db_setting.my_db(sql)):  # 查询是否含有此文章id
                    if(user_id):
                        sql2 = "select view_count from article_views where user_id='%s' and article_id='%s'" % (user_id,article_id)  # 查询数据库表中是否有记录
                        if(db_setting.my_db(sql2)):#查询是否有用户浏览记录
                            update_time = datetime.utcnow()
                            view_count= db_setting.my_db(sql2)[0][0] + 1
                            sql3="UPDATE article_views SET view_count='%s',update_time = '%s' WHERE user_id = '%s' and article_id='%s'" % (
                                    view_count,update_time, user_id,article_id)
                            db_setting.my_db(sql3)
                            return {"code": 200, "message": "浏览记录增加成功","success":"true"}
                        else:
                            create_time = datetime.utcnow()
                            sql4 = "INSERT INTO article_views (user_id, article_id, view_count, create_time, update_time) VALUES ( '%s', '%s', '%s', '%s', '%s')" % (
                                user_id, article_id, 1, create_time, create_time)
                            db_setting.my_db(sql4)
                            return {"code": 200, "message": '新增浏览记录成功',"success":"true"}
                    else:
                        sql2 = "select view_count from article_views where user_id is null and article_id='%s'" % (article_id)  # 查询数据库表中是否有记录
                        if (db_setting.my_db(sql2)):  # 查询是否有游客用户浏览记录
                            update_time = datetime.utcnow()
                            view_count = db_setting.my_db(sql2)[0][0] + 1
                            sql3 = "UPDATE article_views SET view_count='%s',update_time = '%s' WHERE user_id is null and article_id='%s'" % (
                                view_count, update_time,article_id)
                            db_setting.my_db(sql3)
                            return {"code": 200, "message": "游客浏览记录增加成功","success":"true"}
                        else:
                            create_time = datetime.utcnow()
                            sql4 = "INSERT INTO article_views ( article_id, view_count, create_time, update_time) VALUES (  '%s', '%s', '%s', '%s')" % (
                                 article_id, 1, create_time, create_time)
                            db_setting.my_db(sql4)
                            return {"code": 200, "message": '新增游客浏览记录成功',"success":"true"}
                else:
                    return {"code": 500, "message": '不存在的文章',"success":"false"}
            else:
                return {"code": 500, "message": 'article_id字段不能为空',"success":"false"}

    @app.route('/views_count', methods=['get'])
    def views_count():#查询文章的浏览量
        article_id = request.values.get('article_id')  # 文章id
        sql="select sum(view_count) from article_views where article_id='%s'"%(article_id)
        print(db_setting.my_db(sql)[0][0])
        tinydict = {'article_id': '','views_count':''}
        tinydict['article_id']=article_id
        class DecimalEncoder(json.JSONEncoder):#Decimal类型转换方法,count函数的数据转换为int类型
            def default(self, o):
                if isinstance(o, decimal.Decimal):
                    return int(o)
                super(DecimalEncoder, self).default(o)
        views_count= db_setting.my_db(sql)[0][0]
        tinydict['views_count']=views_count
        return {"code": 200, "message": "ok", "data": tinydict, "success": "true"}
        # return Response(json.dumps(tinydict,ensure_ascii=False,cls=DecimalEncoder),mimetype='application/json')

    @app.route('/views_list', methods=['get'])
    def views_list():  # 查询用户浏览列表
        token = request.headers['access_token']  # 获取header里的token
        parse_token = security.parse_token(token)  # 解析token
        if (parse_token == 1):
            return {"code": 1, "message": "token已过期","success": "false"}
        elif (parse_token == 2):
            return {"code": 2, "message": "token认证失败","success": "false"}
        elif (parse_token == 3):
            return {"code": 3, "message": "非法的token","success": "false"}
        else:
            userid = (parse_token['data']['userid'])  # 查询用户id
            sql = "select  a.user_id,b.id,b.article_title,author_id,article_content,view_status,b.create_time as article_createtime,a.update_time as views_time from article_views as a INNER JOIN article as b on a.article_id=b.id and a.user_id='%s' and is_delete!=1  and article_id not in(select article_id from article_views as a INNER JOIN article as b on a.article_id=b.id and user_id!=author_id and view_status=0 and user_id='%s')ORDER BY views_time DESC" % (
                userid,userid)
            dict = {'user_id': '', 'article_id': '', 'article_title': '', 'author_id': '', 'article_content': '',
                    'view_status': '', 'article_create_time': '','views_time':''}
            views_list = list_method.list_method(sql, dict)
            resp = []
            for num in views_list:
                for i in num.keys():
                    if (i == 'author_id'):
                        url = 'http://127.0.0.1:8998/get_avatar'
                        params = {'user_id': num[i]}
                        headers = {'access_token': token}
                        data_m = requests.get(url=url, params=params, headers=headers)
                        resp.append(data_m.json()['data'])
            last_list = splicing_list.splicing_list(views_list, resp)
            return {"code": 200, "message": "ok", "data": last_list, "success": "true"}

            # return Response(json.dumps(views_list, ensure_ascii=False), mimetype='application/json')
