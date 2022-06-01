from flask import Flask,request,Response,render_template
from werkzeug.utils import secure_filename
import os
import uuid
from flaskr.common_method import security,db_setting
from datetime import datetime
from PIL import Image,ExifTags
def upload_avatar(app):
    allow_format = ['png', 'jpg', 'jpeg']  # 允许图片上传格式
    upload_folder = './static/avatar_images/'
    image_url = 'http://127.0.0.1:8998/static/avatar_images/'
    # def after_request(Response):  # 跨域支持
    #     Response.header['Access-Control-Allow-Origin'] = '*'
    #     return Response

    # 判断文件后缀是否在列表中
    def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[-1] in allow_format
    # app.after_request(after_request)
    @app.route('/upload_avatar', methods=['post'])#更新用户头像接口
    def upload_avatar():  # 用户头像上传
        avatar_image = request.files['file']
        if avatar_image and allowed_file(avatar_image.filename):
            # secure_filename方法会去掉文件名中的中文，获取文件的后缀名
            file_suffix = secure_filename(avatar_image.filename).split('.')[-1]#获取文件后缀，即后缀.jpg，.jpeg等
            first_name = str(uuid.uuid4())#uuid生成唯一的名称编码
            # # 将 uuid和后缀拼接为完整的文件名
            file_name = first_name + '.' + file_suffix
            avatar_image.save(os.path.join(upload_folder, file_name))#保存图片到指定目录
            token = request.headers['access_token']  # 获取header里的token
            parse_token = security.parse_token(token)  # 解析token
            image_fullpath=image_url + file_name#拼接完整路径用来保存数据库中
            create_time=datetime.utcnow()
            if (parse_token == 1):
                return {"code": 1, "message": "token已过期", "success": "false"}
            elif (parse_token == 2):
                return {"code": 2, "message": "token认证失败", "success": "false"}
            elif (parse_token == 3):
                return {"code": 3, "message": "非法的token", "success": "false"}
            else:
                userid = (parse_token['data']['userid'])  # 查询用户id
                sql="INSERT INTO user_avatar_image (`user_id`, `avatar_image_url`, `create_time`,'avatar_status') VALUES ('%s', '%s', '%s',1)"%(userid,image_fullpath,create_time)
                db_setting.my_db(sql)
                return {"code": '200', "image_url": image_url + file_name, "message": "上传成功", "success": "true"}
        else:
            return {"code": 500, "message": "格式错误，仅支持jpg、png、jpeg格式文件","success":"false"}


# from flask import Flask, request, Response, render_template
# from werkzeug.utils import secure_filename
# import os
# import uuid
# from PIL import Image, ExifTags
#
# app = Flask(__name__)  # 实例Flask应用
# # 设置允许上传的文件格式
# ALLOW_EXTENSIONS = ['png', 'jpg', 'jpeg']
# # 设置图片保存文件夹
# app.config['UPLOAD_FOLDER'] = './static/image/'
# # 设置图片返回的域名前缀
# image_url = "http://127.0.0.1:8002/image/"
# # 设置图片压缩尺寸
# image_c = 1000
#
#
# # 跨域支持
# def after_request(resp):
#     resp.headers['Access-Control-Allow-Origin'] = '*'
#     return resp
#
#
# app.after_request(after_request)
#
#
# # 判断文件后缀是否在列表中
# def allowed_file(filename):
#     return '.' in filename and filename.rsplit('.', 1)[-1] in ALLOW_EXTENSIONS
#
#
# # 首页
# @app.route('/')
# def hello_world():
#     return render_template('index.html')
#
#
# # 心跳检测
# @app.route("/check", methods=["GET"])
# def check():
#     return 'Im live'
#
#
# # 图片获取地址 用于存放静态文件
# @app.route("/image/<imageId>")
# def get_frame(imageId):
#     # 图片上传保存的路径
#     try:
#         with open(r'./static/image/{}'.format(imageId), 'rb') as f:
#             image = f.read()
#             result = Response(image, mimetype="image/jpg")
#             return result
#     except BaseException as e:
#         return {"code": '503', "data": str(e), "message": "图片不存在"}
#
#
# # 上传图片
# @app.route("/upload_image", methods=['POST', "GET"])
# def uploads():
#     if request.method == 'POST':
#         # 获取文件
#         file = request.files['file']
#         # 检测文件格式
#         if file and allowed_file(file.filename):
#             # secure_filename方法会去掉文件名中的中文，获取文件的后缀名
#             file_name_hz = secure_filename(file.filename).split('.')[-1]
#             # 使用uuid生成唯一图片名
#             first_name = str(uuid.uuid4())
#             # 将 uuid和后缀拼接为 完整的文件名
#             file_name = first_name + '.' + file_name_hz
#             # 保存原图
#             file.save(os.path.join(app.config['UPLOAD_FOLDER'], file_name))
#             # 以下是压缩图片的过程，在原图的基础上
#             file_min = Image.open(file)
#             # exif读取原始方位信息 防止图片压缩后发生旋转
#             try:
#                 for orientation in ExifTags.TAGS.keys():
#                     if ExifTags.TAGS[orientation] == 'Orientation': break
#                 exif = dict(file_min._getexif().items())
#                 if exif[orientation] == 3:
#                     file_min = file_min.rotate(180, expand=True)
#                 elif exif[orientation] == 6:
#                     file_min = file_min.rotate(270, expand=True)
#                 elif exif[orientation] == 8:
#                     file_min = file_min.rotate(90, expand=True)
#             except:
#                 pass
#             # 获取原图尺寸
#             w, h = file_min.size
#             # 计算压缩比
#             bili = int(w / image_c)
#             # 按比例对宽高压缩
#             file_min.thumbnail((w // bili, h // bili))
#             # 生成缩略图的完整文件名
#             file_name_min = first_name + '_min.' + file_name_hz
#             # 保存缩略图
#             file_min.save(os.path.join(app.config['UPLOAD_FOLDER'], file_name_min))
#             # 返回原本和缩略图的 完整浏览链接
#             return {"code": '200', "image_url": image_url + file_name, "image_url_min": image_url + file_name_min,
#                     "message": "上传成功"}
#         else:
#             return "格式错误，仅支持jpg、png、jpeg格式文件"
#     return {"code": '503', "data": "", "message": "仅支持post方法"}
#
#
# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=8002, debug=True)  # 项目入口