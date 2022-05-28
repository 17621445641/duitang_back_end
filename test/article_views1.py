from flask_restful import reqparse,Resource
class article_views(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('article_id',required=True,help='必填')
        args=parser.parse_args()
        print(args.article_id)
        return {"username":"bj"}
# def article_views(app):
#     @app.route('/article_views', methods=['get'])
#     def article_views():
#         token = request.headers['access_token']  # 获取header里的token
#         parse_token = security.parse_token(token)  # 解析token
#         if (parse_token == 1):
#             return 'token已过期'
#         elif (parse_token == 2):
#             return 'token认证失败'
#         elif (parse_token == 3):
#             return '非法的token'
#         else:
#             userid = (parse_token['data']['userid'])  # 查询用户id
#             article_id = request.values.get('article_id')  # 文章id
#             if (article_id):  # 判断是否传了article_id字段
#                 sql = "select id from article where id='%s'" % (article_id)
#                 if (db_setting.my_db(sql)):  # 查询是否含有此文章id
#                     sql2 = "select view_count from article_views where user_id='%s' and article_id='%s'" % (userid,article_id)  # 查询数据库表中是否有记录
#                     if(db_setting.my_db(sql2)):#查询是否有用户浏览记录
#                         update_time = datetime.utcnow()
#                         view_count=db_setting.my_db(sql2)[0][0]+1
#                         sql3="UPDATE article_views SET view_count='%s',update_time = '%s' WHERE user_id = '%s' and article_id='%s'" % (
#                                 view_count,update_time, userid,article_id)
#                         db_setting.my_db(sql3)
#                         return "浏览记录增加成功"
#                     else:
#                         create_time = datetime.utcnow()
#                         sql4 = "INSERT INTO article_views (user_id, article_id, view_count, create_time, update_time) VALUES ( '%s', '%s', '%s', '%s', '%s')" % (
#                             userid, article_id, 1, create_time, create_time)
#                         db_setting.my_db(sql4)
#                         return '新增浏览记录成功'
#                 else:
#                     return '不存在的文章'
#             else:
#                 return 'article_id字段不能为空'
#
#     @app.route('/views_count', methods=['get'])
#     def views_count():#查询文章的浏览量
#         # article_id = request.values.get('article_id')  # 文章id
#         parser=reqparse.RequestParser()
#         parser.add_argument('article_id',required=True,help='必填')
#         args=parser.parse_args()
#         print(args.article_id)
#         return "t"
