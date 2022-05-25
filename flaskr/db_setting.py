import pymysql
# db_host='127.0.0.1',
# db_user='root',
# db_pwd='123456',
# db_name='myproject',
# db_port=3306,
# db_charset='utf8',
# sql='SELECT * from user_message '
def my_db(sql):
    conn = pymysql.connect(host='127.0.0.1', user='root', password='123456', db='myproject',
                           port=3306, charset='utf8', autocommit=True)
    cur = conn.cursor()
    cur.execute(sql)
    res = cur.fetchall()
    cur.close()
    conn.close()
    return (res)
# if __name__ == '__main__':
#     my_db(sql)