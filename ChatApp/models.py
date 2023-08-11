import pymysql
from util.DB import DB


class dbConnect:
    """
    ユーザー
    """
    def createUser(user_id, user_name, email, password):
        try:
            connection = DB.getConnection()
            cursor = connection.cursor()
            sql = "INSERT INTO users (id, user_name, email, password) VALUES (%s, %s, %s, %s);"
            cursor.execute(sql, (user_id, user_name, email, password))
            connection.commit()
        except Exception as err:
            print(err + 'が発生しています')
            abort(500)
        finally:
            cursor.close()

    # getUser -> getUserById, getUserByEmail に拡張
    def getUserById(user_id):
        try:
            connection = DB.getConnection()
            cursor = connection.cursor()
            sql = "SELECT * FROM users WHERE id=%s;"
            cursor.execute(sql, (user_id))
            user = cursor.fetchone()
            return user
        except Exception as err:
            print(err + 'が発生しています')
            abort(500)
        finally:
            cursor.close()

    def getUserByEmail(email):
        try:
            connection = DB.getConnection()
            cursor = connection.cursor()
            sql = "SELECT * FROM users WHERE email=%s;"
            cursor.execute(sql, (email))
            user = cursor.fetchone()
            return user
        except Exception as err:
            print(err + 'が発生しています')
            abort(500)
        finally:
            cursor.close()

    """
    フレンド
    """
    def createFriendRequest(sender_id, receiver_id):
        try:
            connection = DB.getConnection()
            cursor = connection.cursor()

            # 既に申請済みかどうかをチェックするクエリ
            sql = "SELECT * FROM friend_requests WHERE sender_id = %s AND receiver_id = %s"
            cursor.execute(sql, (sender_id, receiver_id))
            existing_request = cursor.fetchone()

            # 既に申請済みの場合は'duplicate'を返す
            if existing_request:
                return 'duplicate'

            # 申請が重複していない場合、新しいフレンド申請を作成する
            sql = "INSERT INTO friend_requests(sender_id, receiver_id) VALUES(%s, %s)"
            cursor.execute(sql, (sender_id, receiver_id))
            connection.commit()

            # 成功した場合は'success'を返す
            return 'success'

        except Exception as err:
            print(err, 'が発生しています')
            # エラーが発生した場合は'error'を返す
            return 'error'
        finally:
            cursor.close()

    def getFriendReqList(receiver_id):
        try:
            conn = DB.getConnection()
            cur = conn.cursor()

            # 友達申請一覧を取得するクエリ
            sql = "SELECT fr.sender_id,u1.user_name as sender_name,fr.created_at \
                FROM friend_requests fr INNER JOIN users u1 on sender_id = u1.id \
                WHERE fr.receiver_id=%s;"
            
            cur.execute(sql, (receiver_id))
            friend_requests = cur.fetchall()

            return friend_requests
        
        except Exception as e:
            print(e + "が発生しています")
            abort(500)
        finally:
            cur.close()

    """
    チャンネル
    """
    def getChannelAll():
        try:
            connection = DB.getConnection()
            cursor = connection.cursor()
            sql = "SELECT * FROM channels;"
            cursor.execute(sql)
            channels = cursor.fetchall()
            return channels
        except Exception as err:
            print(err + 'が発生しています')
            abort(500)
        finally:
            cursor.close()

    def getChannelById(channel_id):
        try:
            connection = DB.getConnection()
            cursor = connection.cursor()
            sql = "SELECT * FROM channels WHERE id=%s;"
            cursor.execute(sql, (channel_id))
            channel = cursor.fetchone()
            return channel
        except Exception as err:
            print(err + 'が発生しています')
            abort(500)
        finally:
            cursor.close()

    def getChannelByName(channel_name):
        try:
            connection = DB.getConnection()
            cursor = connection.cursor()
            sql = "SELECT * FROM channels WHERE channel_name=%s;"
            cursor.execute(sql, (channel_name))
            channel = cursor.fetchone()
            return channel
        except Exception as err:
            print(err + 'が発生しています')
            abort(500)
        finally:
            cursor.close()

    def addChannel(user_id, newChannelName, newChannelDescription):
        try:
            connection = DB.getConnection()
            cursor = connection.cursor()
            sql = "INSERT INTO channels (id, name, abstract) VALUES (%s, %s, %s);"
            cursor.execute(
                sql, (user_id, newChannelName, newChannelDescription))
            connection.commit()
        except Exception as err:
            print(err + 'が発生しています')
            abort(500)
        finally:
            cursor.close()

    def getChannelByName(channel_name):
        try:
            connection = DB.getConnection()
            cursor = connection.cursor()
            sql = "SELECT * FROM channels WHERE channel_name=%s;"
            cursor.execute(sql, (channel_name))
            channel = cursor.fetchone()
        except Exception as err:
            print(err + 'が発生しました')
            abort(500)
        finally:
            cursor.close()
            return channel

    def updateChannel(user_id, newChannelName, newChannelDescription, channel_id):
        try:
            connection = DB.getConnection()
            cursor = connection.cursor()
            sql = "UPDATE channels SET uid=%s, name=%s, abstract=%s WHERE id=%s;"
            cursor.execute(sql, (user_id, newChannelName,
                           newChannelDescription, channel_id))
            connection.commit()
        except Exception as err:
            print(err + 'が発生しました')
            abort(500)
        finally:
            cursor.close()

    def deleteChannel(channel_id):
        try:
            connection = DB.getConnection()
            cursor = connection.cursor()
            sql = "DELETE FROM channels WHERE id=%s;"
            cursor.execute(sql, (channel_id))
            connection.commit()
        except Exception as err:
            print(err + 'が発生しています')
            abort(500)
        finally:
            cursor.close()

    """
    メッセージ
    """
    def getMessageAll(channel_id):
        try:
            connection = DB.getConnection()
            cursor = connection.cursor()
            sql = "SELECT id,u.uid, user_name, message FROM messages AS m INNER JOIN users AS u ON m.uid = u.uid WHERE cid = %s;"
            cursor.execute(sql, (channel_id))
            messages = cursor.fetchall()
            return messages
        except Exception as err:
            print(err + 'が発生しています')
            abort(500)
        finally:
            cursor.close()

    def createMessage(user_id, channel_id, message):
        try:
            connection = DB.getConnection()
            cursor = connection.cursor()
            sql = "INSERT INTO messages(uid, cid, message) VALUES(%s, %s, %s)"
            cursor.execute(sql, (user_id, channel_id, message))
            connection.commit()
        except Exception as err:
            print(err + 'が発生しています')
            abort(500)
        finally:
            cursor.close()

    def deleteMessage(message_id):
        try:
            connection = DB.getConnection()
            cursor = connection.cursor()
            sql = "DELETE FROM messages WHERE id=%s;"
            cursor.execute(sql, (message_id))
            connection.commit()
        except Exception as err:
            print(err + 'が発生しています')
            abort(500)
        finally:
            cursor.close()
