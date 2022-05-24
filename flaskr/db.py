import pymysql
account='17600000000'
sql="SELECT * from user_account where account='%s' " % (account)
def my_db(sql):
    conn=pymysql.connect(host='127.0.0.1',user='root',password='123456',db='myproject',
                port=3306,charset='utf8',autocommit=True)
    cur=conn.cursor()
    cur.execute(sql)
    res=cur.fetchall()
    print(res)
    if(len(res)!=0):
        print(1)
    else:
        print('用户暂未注册')
    cur.close()
    conn.close()
    return res
if __name__ == '__main__':
    my_db(sql)



