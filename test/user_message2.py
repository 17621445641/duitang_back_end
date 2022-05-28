from flask import request
from flaskr.common_method import security


def ww(server):
# server=Flask(__name__)
    @server.route('/userinfo',methods=['get'])
    def userinfo():
        token = request.headers['access_token']  # 获取header里的token
        parse_token= security.parse_token(token)
        return security.parse_token(parse_token)
    # if __name__ == '__main__':
    #     server.run(host='127.0.0.1',port=8998,debug=True)
