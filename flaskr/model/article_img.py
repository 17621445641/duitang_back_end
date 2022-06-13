from flask import Flask,request,Response,render_template
from werkzeug.utils import secure_filename
import os
import uuid
from flaskr.common_method import security,db_setting
from datetime import datetime
from PIL import Image,ExifTags
def upload_article_img(app):
    allow_format = ['png', 'jpg', 'jpeg']  # 允许图片上传格式
    upload_folder = './static/article_img/'
    image_url = 'http://127.0.0.1:8998/static/article_img/'
    # def after_request(resp):  # 跨域支持
    #     resp.header['Access-Control-Allow-Origin'] = '*'
    #     return resp
    #
    # app.after_request(after_request)
    # 判断文件后缀是否在列表中
    def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[-1] in allow_format

    @app.route('/article_img', methods=['post'])#更新用户头像接口
    def article_img():  # 用户头像上传
        avatar_image = request.files['file']
        print(avatar_image)
        if avatar_image and allowed_file(avatar_image.filename):
            # secure_filename方法会去掉文件名中的中文，获取文件的后缀名
            file_suffix = secure_filename(avatar_image.filename).split('.')[-1]#获取文件后缀，即后缀.jpg，.jpeg等
            first_name = str(uuid.uuid4())#uuid生成唯一的名称编码
            # # 将 uuid和后缀拼接为完整的文件名
            file_name = first_name + '.' + file_suffix

            avatar_image.save(os.path.join(upload_folder, file_name))#保存图片到指定目录
            token = request.headers['access_token']  # 获取header里的token
            # print(token)
            parse_token = security.parse_token(token)  # 解析token
            image_fullpath=image_url + file_name
            # all_image_fullpath=image_url+image_fullpath#拼接完整路径用来保存数据库中
            # image_fullpath=
            create_time=datetime.utcnow()
            if (parse_token == 1):
                return {"code": 1, "message": "token已过期", "success": "false"}
            elif (parse_token == 2):
                return {"code": 2, "message": "token认证失败", "success": "false"}
            elif (parse_token == 3):
                return {"code": 3, "message": "非法的token", "success": "false"}
            else:
                userid = (parse_token['data']['userid'])  # 查询用户id
                sql="INSERT INTO user_avatar_image (`user_id`, `avatar_image_url`, `create_time`) VALUES ('%s', '%s', '%s')"%(userid,image_fullpath,create_time)
                db_setting.my_db(sql)
                return {"code": '200', "image_url": image_url + file_name, "message": "上传成功", "success": "true"}
        else:
            return {"code": 500, "message": "格式错误，仅支持jpg、png、jpeg格式文件","success":"false"}