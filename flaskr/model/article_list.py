from flask import request
from datetime import datetime,timedelta
from flaskr.common_method import db_setting, security,list_method
import random
def article_list(app):
    @app.route('/article_list', methods=['get'])
    def article_list():  # 首页推荐文章列表
        sql="select id,article_title,author_id,article_content,create_time,article_img from article where view_status=1 and article_type=2"
        dict = { 'article_id': '', 'article_title': '', 'author_id': '', 'article_content': '',
                 'article_create_time': '', "article_imglist":''}
        # article_list=db_setting.my_db(sql)
        article_list=list_method.list_method(sql,dict)
        return {"code": 200, "message": "ok","data":article_list,"success":"true"}
