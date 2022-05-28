import decimal
from flask import request,Response
from datetime import datetime
import json
from flaskr.common_method import db_setting,security,list_method


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
                            return "浏览记录增加成功"
                        else:
                            create_time = datetime.utcnow()
                            sql4 = "INSERT INTO article_views (user_id, article_id, view_count, create_time, update_time) VALUES ( '%s', '%s', '%s', '%s', '%s')" % (
                                user_id, article_id, 1, create_time, create_time)
                            db_setting.my_db(sql4)
                            return '新增浏览记录成功'
                    else:
                        sql2 = "select view_count from article_views where user_id is null and article_id='%s'" % (article_id)  # 查询数据库表中是否有记录
                        if (db_setting.my_db(sql2)):  # 查询是否有游客用户浏览记录
                            update_time = datetime.utcnow()
                            view_count = db_setting.my_db(sql2)[0][0] + 1
                            sql3 = "UPDATE article_views SET view_count='%s',update_time = '%s' WHERE user_id is null and article_id='%s'" % (
                                view_count, update_time,article_id)
                            db_setting.my_db(sql3)
                            return "游客浏览记录增加成功"
                        else:
                            create_time = datetime.utcnow()
                            sql4 = "INSERT INTO article_views ( article_id, view_count, create_time, update_time) VALUES (  '%s', '%s', '%s', '%s')" % (
                                 article_id, 1, create_time, create_time)
                            db_setting.my_db(sql4)
                            return '新增游客浏览记录成功'
                else:
                    return '不存在的文章'
            else:
                return 'article_id字段不能为空'

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
        return Response(json.dumps(tinydict,ensure_ascii=False,cls=DecimalEncoder),mimetype='application/json')

    @app.route('/views_list', methods=['get'])
    def views_list():  # 查询用户浏览列表
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
            sql = "select  a.user_id,b.id,b.article_title,author_id,article_content,view_status,b.create_time,b.update_time from article_views as a INNER JOIN article as b on a.article_id=b.id and a.user_id='%s' and article_id not in(select article_id from article_views as a INNER JOIN article as b on a.article_id=b.id and user_id!=author_id and view_status=0 and user_id='%s')" % (
                userid,userid)
            dict = {'user_id': '', 'article_id': '', 'article_title': '', 'author_id': '', 'article_content': '',
                    'view_status': '', 'create_time': ''}
            views_list = list_method.list_method(sql, dict)
            return Response(json.dumps(views_list, ensure_ascii=False), mimetype='application/json')
