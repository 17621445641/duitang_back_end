from flask import Flask,request
from datetime import datetime
import security
import db_setting
def article_like(app):
    @app.route('/article_like', methods=['post'])
    def dislike_like():  # 文章喜欢和取消喜欢
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
            status = request.json.get('status')  # 根据status执行喜欢或者不喜欢
            if (article_id):  # 判断是否传了article_id字段
                sql = "select id from article where id='%s'" % (article_id)
                if (db_setting.my_db(sql)):  # 查询是否含有此文章id
                    sql2 = "select like_status from article_like where user_id='%s'" % (userid)#查询数据库表中是否有记录
                    if(status==0): #判断执行取消喜欢
                        if (db_setting.my_db(sql2) and db_setting.my_db(sql2)[0][0] == 1):  # 查询是否用户已喜欢，未有记录则插入一条喜欢记录,已有记录且状态为未喜欢，则进行喜欢
                            update_time = datetime.utcnow()
                            sql3 = "UPDATE article_like SET like_status=0,update_time = '%s' WHERE user_id = '%s'" % (
                            update_time, userid)
                            db_setting.my_db(sql3)
                            return "取消喜欢成功"
                        else:
                            return "取消喜欢失败,未找到记录"
                    elif(status==1):#判断执行喜欢
                        if (db_setting.my_db(sql2) and db_setting.my_db(sql2)[0][0] == 0):
                            update_time = datetime.utcnow()
                            sql3 = "UPDATE article_like SET like_status=1,update_time = '%s' WHERE user_id = '%s'" % (
                                update_time, userid)
                            db_setting.my_db(sql3)
                            return "更新喜欢成功"
                        elif(db_setting.my_db(sql2) and db_setting.my_db(sql2)[0][0] == 1):
                            return "喜欢失败,已喜欢"
                        else:
                            create_time = datetime.utcnow()
                            sql4 = "INSERT INTO article_like (user_id, article_id, like_status, create_time, update_time) VALUES ( '%s', '%s', '%s', '%s', '%s')" % (
                            userid, article_id, 1, create_time, create_time)
                            db_setting.my_db(sql4)
                            return '新增喜欢成功'
                    else:
                        return "请输入正确的状态码(0取消喜欢，1喜欢)"
                else:
                    return '不存在的文章'
            else:
                return 'article_id字段不能为空'

    @app.route('/like_list', methods=['get'])
    def like_list():  # 喜欢列表
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
            sql="select  a.user_id,b.id,b.article_title,author_id,article_content,view_status,b.create_time,b.update_time from article_like as a INNER JOIN article as b on a.article_id=b.id and a.like_status=1 and a.user_id='%s'"%(userid)
            res=db_setting.my_db(sql)
            print (res)
            return res