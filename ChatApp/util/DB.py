import pymysql


class DB:
    def getConnection():
        try:
            connection = pymysql.connect(
                host="db",
                db="chatapp",
                user="testuser",
                password="testuser",
                charset="utf8",
                cursorclass=pymysql.cursors.DictCursor
            )
            return connection
        except (ConnectionError):
            print("コネクションエラーです")
            connection.close()
