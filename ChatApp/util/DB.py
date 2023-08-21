import pymysql


class DB:
    def getConnection():
        try:
            connection = pymysql.connect(
                host="chatapp.ci06votjyvzz.ap-northeast-1.rds.amazonaws.com",
                db="chatapp",
                user="admin",
                password="hJpQ9B4A",
                charset="utf8",
                cursorclass=pymysql.cursors.DictCursor
            )
            return connection
        except (ConnectionError):
            print("コネクションエラーです")
            connection.close()
