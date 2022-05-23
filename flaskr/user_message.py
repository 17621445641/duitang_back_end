import flask
import db
import json
server=flask.Flask(__name__)
sql='SELECT * from user_message '
@server.route('/login',methods=['get'])
def login():
    res1=db.my_db(sql)
    if res1:
        # res={"msg":"正确"}
        res=res1[0][2]
        # print(1)
    else:
        res={"msg":'错误'}
        # print(2)
    return json.dumps(res,ensure_ascii=False,indent=4)
server.run(host='127.0.0.1',port=8998,debug=True)
# from flask import Flask
#
# app = Flask(__name__)
#
# @app.route("/")
# def hello_world():
#     return "<p>Hello, World!</p>"
