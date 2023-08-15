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
            print(err + "が発生しています")
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
            print(err + "が発生しています")
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
            print(err + "が発生しています")
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
                return "duplicate"

            # 申請が重複していない場合、新しいフレンド申請を作成する
            sql = "INSERT INTO friend_requests(sender_id, receiver_id) VALUES(%s, %s)"
            cursor.execute(sql, (sender_id, receiver_id))
            connection.commit()

            # 成功した場合は'success'を返す
            return "success"

        except Exception as err:
            print(err, "が発生しています")
            # エラーが発生した場合は'error'を返す
            return "error"
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
            print(err + "が発生しています")
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
            print(err + "が発生しています")
            abort(500)
        finally:
            cursor.close()

    def getChannelByName(channel_name):
        try:
            connection = DB.getConnection()
            cursor = connection.cursor()
            sql = "SELECT * FROM channels WHERE name=%s;"
            cursor.execute(sql, (channel_name))
            channel = cursor.fetchone()
            return channel
        except Exception as err:
            print(err + "が発生しています")
            abort(500)
        finally:
            cursor.close()

    def getChannels(user_id, channnel_type):
        try:
            connection = DB.getConnection()
            cursor = connection.cursor()
            sql = "SELECT c.* FROM channels as c INNER JOIN channel_users as cu ON c.id = cu.channel_id\
                    WHERE cu.user_id = %s AND c.type = %s ORDER BY c.updated_at DESC;"
            cursor.execute(sql, (user_id, channnel_type))
            channel = cursor.fetchall()
            return channel
        except Exception as err:
            print(err + "が発生しています")
            abort(500)
        finally:
            cursor.close()

    # channelsテーブルにレコードを挿入し、挿入したchannel_idを取得する
    def addChannelGetId(newChannelName, newChannelDescription, channelType):
        try:
            connection = DB.getConnection()
            # チャンネル情報をchannelsテーブルに挿入
            cursor = connection.cursor()
            sql = "INSERT INTO channels (name, abstract, type) VALUES (%s, %s, %s);"
            cursor.execute(sql, (newChannelName, newChannelDescription, channelType))
            connection.commit()

            # 挿入したチャンネル情報のidを取得
            cursor2 = connection.cursor()
            sql2 = "SELECT LAST_INSERT_ID() as current_id;"
            cursor2.execute(sql2)
            id = cursor2.fetchall()
            return id

        except Exception as err:
            print(err + "が発生しています")
            abort(500)
        finally:
            cursor.close()

    # channel_usersテーブルにレコードを挿入
    def addChannelUser(channel_id, user_id, role):
        try:
            connection = DB.getConnection()
            cursor = connection.cursor()
            sql = "INSERT INTO channel_users (channel_id, user_id, role) VALUES (%s, %s, %s);"
            cursor.execute(sql, (channel_id, user_id, role))
            connection.commit()
        except Exception as err:
            print(err + "が発生しました")
            abort(500)
        finally:
            cursor.close

    def updateChannel(user_id, newChannelName, newChannelDescription, channel_id):
        try:
            connection = DB.getConnection()
            cursor = connection.cursor()
            sql = "UPDATE channels SET uid=%s, name=%s, abstract=%s WHERE id=%s;"
            cursor.execute(
                sql, (user_id, newChannelName, newChannelDescription, channel_id)
            )
            connection.commit()
        except Exception as err:
            print(err + "が発生しました")
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
            print(err + "が発生しています")
            abort(500)
        finally:
            cursor.close()

    """
    グループ
    """

    def getFriendsList(user_id, user_id2):
        try:
            conn = DB.getConnection()
            cur = conn.cursor()
            sql = "SELECT fr1.friend_id,u1.user_name \
                    FROM friends fr1 INNER JOIN users u1 on friend_id = u1.id \
                    WHERE fr1.user_id=%s \
                    UNION SELECT fr1.user_id,u1.user_name \
                    FROM friends fr1 INNER JOIN users u1 on user_id = u1.id \
                    WHERE fr1.friend_id=%s \
                    ORDER BY user_name;"
            cur.execute(sql, (user_id, user_id2))
            friends = cur.fetchall()
            return friends
        except Exception as e:
            print(e + "が発生しています")
            abort(500)
        finally:
            cur.close()

    def add_group_Channel(newChannelName, newChannelDescription, newChannelType):
        try:
            conn = DB.getConnection()
            cur = conn.cursor()
            sql = "INSERT INTO channels (name, abstract, type) VALUES (%s, %s, %s);"
            cur.execute(sql, (newChannelName, newChannelDescription, newChannelType))
            conn.commit()
        except Exception as e:
            print(e + "が発生しています")
            abort(500)
        finally:
            cur.close()

    def add_group_Channel_adminUser(channel_id, adminUid, adminRole):
        try:
            conn = DB.getConnection()
            cur = conn.cursor()
            sql = "INSERT INTO channel_users (channel_id, user_id, role) VALUES (%s, %s, %s);"
            cur.execute(sql, (channel_id, adminUid, adminRole))
            conn.commit()
        except Exception as e:
            print(e + "が発生しています")
            abort(500)
        finally:
            cur.close()

    def add_group_Channel_Users(channel_id, friend_id, memberRole):
        try:
            conn = DB.getConnection()
            cur = conn.cursor()
            sql = "INSERT INTO channel_users (channel_id, user_id, role) VALUES (%s, %s, %s);"
            cur.execute(sql, (channel_id, friend_id, memberRole))
            conn.commit()
        except Exception as e:
            print(e + "が発生しています")
            abort(500)
        finally:
            cur.close()

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
            print(err + "が発生しています")
            abort(500)
        finally:
            cursor.close()

    def createMessage(user_id, channel_id, message, type):
        try:
            connection = DB.getConnection()
            cursor = connection.cursor()
            sql = "INSERT INTO messages(channel_id, user_id, message, type) VALUES(%s, %s, %s, %s)"
            cursor.execute(sql, (user_id, channel_id, message, type))
            connection.commit()
        except Exception as err:
            print(err + "が発生しています")
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
            print(err + "が発生しています")
            abort(500)
        finally:
            cursor.close()
