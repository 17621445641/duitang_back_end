import json
import random

from flask import request,Response
from datetime import datetime
from flaskr.common_method import db_setting, security,list_method,splicing_list
def article_details(app):
    @app.route('/article_details', methods=['get'])
    def article_details():
        article_id=request.values.get('article_id')
        user_id = request.values.get('user_id')
        sql="SELECT id,article_title,author_id,article_content,create_time,article_img FROM article where id='%s' "% (
            article_id)
        tinydict={'article_id': '', 'article_title': '', 'author_id': '', 'article_content': '', 'create_time': '', 'article_img': ''}
        tinydict2 = {"like_count": ''}
        tinydict3 = {"like_status": ''}
        tinydict4 = {"collect_status": ''}
        sql2="select count(*)as click_count from article_click where article_id='%s' and click_status=1"%(article_id)
        #查询文章喜欢数量
        sql3="select click_status from article_click where article_id='%s' and user_id='%s' and click_status=1"%(article_id,user_id)
        #查询用户是否喜欢该文章
        sql4="select collect_status from article_collect where article_id='%s' and user_id='%s' and collect_status=1"%(article_id,user_id)
        resp = []
        resp2=[]
        resp3=[]
        article_details=list_method.list_method(sql,tinydict)
        click_count=list_method.list_method(sql2,tinydict2)[0]
        click_status = list_method.list_method(sql3,tinydict3)[0]
        collect_status=list_method.list_method(sql4,tinydict4)[0]
        # print(click_status)
        # print(click_status)
        # print(b[0].click_count)
        change_type_article_list =json.dumps(click_count)
        change_type_click_status = json.dumps(click_status)
        change_type_collect_status = json.dumps(collect_status)
        # print(type(change_type))
        resp.append(change_type_article_list)
        last_list1 = splicing_list.splicing_list(article_details, resp)
        resp2.append(change_type_click_status)
        last_list2=splicing_list.splicing_list(last_list1, resp2)
        resp3.append(change_type_collect_status)
        # print(resp3)
        last_list3=splicing_list.splicing_list(last_list2, resp3)
        # print(resp)
        return {"code": 200, "message": "ok", "data": last_list3 ,"success": "true"}