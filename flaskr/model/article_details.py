import random

from flask import request,Response
from datetime import datetime
from flaskr.common_method import db_setting, security,list_method,splicing_list
def article_details(app):
    @app.route('/article_details', methods=['get'])
    def article_details():
        article_id=request.values.get('article_id')
        sql="SELECT id,article_title,author_id,article_content,create_time,article_img FROM article where id='%s'"% (
            article_id)
        tinydict={'article_id': '', 'article_title': '', 'author_id': '', 'article_content': '', 'create_time': '', 'article_img': ''}
        list_method.list_method(sql,tinydict)
        return {"code": 200, "message": "ok", "data": tinydict, "success": "true"}