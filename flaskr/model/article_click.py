from flask import request,Response
from datetime import datetime
from flaskr.common_method import db_setting, security,list_method
import json
def article_click(app):
    @app.route('/article_click', methods=['post'])
    def disclick_click():  # 文章点赞和取消点赞
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
            article_id = request.json.get('article_id')  # 文章id
            status = request.json.get('status')  # 根据status执行点赞或者取消点赞
            if (article_id):  # 判断是否传了article_id字段
                sql = "select id from article where id='%s'" % (article_id)
                if (db_setting.my_db(sql)):  # 查询是否含有此文章id
                    sql2 = "select click_status from article_click where user_id='%s'" % (userid)#查询数据库表中是否有记录
                    if(status==0): #判断为0的时候执行取消点赞
                        if (db_setting.my_db(sql2) and db_setting.my_db(sql2)[0][0] == 1):  # 查询是否用户已点赞，未有记录则插入一条点赞记录,已有记录且状态为未点赞，则进行点赞
                            update_time = datetime.utcnow()
                            sql3 = "UPDATE article_click SET click_status=0,update_time = '%s' WHERE user_id = '%s'" % (
                            update_time, userid)
                            db_setting.my_db(sql3)
                            return "取消点赞成功"
                        elif(db_setting.my_db(sql2) and db_setting.my_db(sql2)[0][0] == 0):
                            return "已取消点赞失败,无法再取消点赞"
                        else:
                            return "取消点赞失败,未找到记录"
                    elif(status==1):#判断为1的时候执行点赞
                        if (db_setting.my_db(sql2) and db_setting.my_db(sql2)[0][0] == 0):
                            update_time = datetime.utcnow()
                            sql3 = "UPDATE article_click SET click_status=1,update_time = '%s' WHERE user_id = '%s'" % (
                                update_time, userid)
                            db_setting.my_db(sql3)
                            return "更新点赞成功"
                        elif(db_setting.my_db(sql2) and db_setting.my_db(sql2)[0][0] == 1):
                            return "点赞失败，已点赞"
                        else:
                            create_time = datetime.utcnow()
                            sql4 = "INSERT INTO article_click (user_id, article_id, click_status, create_time, update_time) VALUES ( '%s', '%s', '%s', '%s', '%s')" % (
                            userid, article_id, 1, create_time, create_time)
                            db_setting.my_db(sql4)
                            return '新增点赞成功'
                    else:
                        return "请输入正确的状态码(0取消点赞，1点赞)"
                else:
                    return '不存在的文章'
            else:
                return 'article_id字段不能为空'

    @app.route('/click_list', methods=['get'])
    def click_list():  # 查询用户点赞列表
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
            sql = "select  a.user_id,b.id,b.article_title,author_id,article_content,view_status,b.create_time,b.update_time from article_click as a INNER JOIN article as b on a.article_id=b.id and a.user_id='%s' and a.click_status=1 and article_id not in(select article_id from article_click as a INNER JOIN article as b on a.article_id=b.id and user_id!=author_id and view_status=0 and user_id='%s')" % (
                userid,userid)
            dict = {'user_id': '', 'article_id': '', 'article_title': '', 'author_id': '', 'article_content': '',
                    'view_status': '', 'create_time': ''}
            like_list = list_method.list_method(sql, dict)
            return Response(json.dumps(like_list, ensure_ascii=False), mimetype='application/json')