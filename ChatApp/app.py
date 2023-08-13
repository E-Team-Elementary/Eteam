from flask import Flask, request, redirect, render_template, session, flash, abort, jsonify
from datetime import timedelta
import hashlib
import uuid
import re

from models import dbConnect

app = Flask(__name__)
app.secret_key = uuid.uuid4().hex
app.permanent_session_lifetime = timedelta(days=30)


"""
ユーザー認証 
"""
# サインアップページの表示


@app.route('/signup')
def signup():
    return render_template('registration/signup.html')


# サインアップ処理
@app.route('/signup', methods=['POST'])
def userSignup():
    user_name = request.form.get('name')
    email = request.form.get('email')
    password1 = request.form.get('password1')
    password2 = request.form.get('password2')

    pattern = "^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"

    if user_name == '' or email == '' or password1 == '' or password2 == '':
        flash('空のフォームがあるようです')
    elif password1 != password2:
        flash('二つのパスワードの値が違っています')
    elif re.match(pattern, email) is None:
        flash('正しいメールアドレスの形式ではありません')
    else:
        user_id = uuid.uuid4()
        password = hashlib.sha256(password1.encode('utf-8')).hexdigest()
        DBuser = dbConnect.getUserByEmail(email)

        if DBuser != None:
            flash('既に登録されているようです')
        else:
            dbConnect.createUser(user_id, user_name, email, password)
            UserId = str(user_id)
            session['user_id'] = UserId
            return redirect('/')
    return redirect('/signup')


# ログインページの表示
@app.route('/login')
def login():
    return render_template('registration/login.html')


# ログイン処理
@app.route('/login', methods=['POST'])
def userLogin():
    email = request.form.get('email')
    password = request.form.get('password')

    if email == '' or password == '':
        flash('空のフォームがあるようです')
    else:
        user = dbConnect.getUserByEmail(email)
        if user is None:
            flash('このユーザーは存在しません')
        else:
            hashPassword = hashlib.sha256(password.encode('utf-8')).hexdigest()
            if hashPassword != user["password"]:
                flash('パスワードが間違っています！')
            else:
                session['user_id'] = user["id"]
                return redirect('/')
    return redirect('/login')


# ログアウト
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')


# ホーム画面の表示
# @app.route('/')
# def index():
#     user_id = session.get("user_id")
#     if user_id is None:
#         return redirect('/login')
#     else:
#         channels = dbConnect.getChannelAll()
#         channels.reverse()
#     return render_template('index.html', channels=channels, user_id=user_id)


"""
フレンド
"""


# Emailでユーザーを検索　（フレンド申請用）
@app.route('/search_user', methods=['POST'])
def search_user():
    # user_id = session.get("user_id")
    # if user_id is None:
    #     return redirect('/login')
    email = request.form.get('email')
    user = dbConnect.getUserByEmail(email)
    if not user:
        # ユーザーが存在しない場合は空のuser_infoを返す
        user_info = {
            'user_id': '',
            'user_name': '',
            'email': '',
        }
    else:
        user_info = {
            'user_id': user['id'],
            'user_name': user['user_name'],
            'email': user['email'],
        }
    return jsonify(user_info), 200  # JSONでユーザー情報を返却


# フレンド申請を作成する
@app.route('/friend_request', methods=['POST'])
def friend_request():
    # user_id = session.get("user_id")
    # if user_id is None:
    #     return redirect('/login')
    data = request.json
    sender_id = data.get('sender_id')
    receiver_id = data.get('receiver_id')
    if sender_id is None or receiver_id is None:
        return jsonify({'error': 'Invalid request data. Missing sender_id or receiver_id.'}), 400
    result = dbConnect.createFriendRequest(sender_id, receiver_id)

    if result == 'success':
        return jsonify({'message': 'フレンド申請を送りました'}), 200
    elif result == 'duplicate':
        return jsonify({'message': '既に申請済みです'}), 422
    elif result == 'error':
        return jsonify({'message': '申請に失敗しました'}), 422


# ログインユーザーに対して、友達申請一覧を取得し、友達申請一覧画面(仮)に遷移
'''
 todo:
 フレンド一覧を取得する時、本来はGetメソッドを指定する予定だが、テスト用にPOSTも指定している
 セッション周りのコメントを外す、POSTを指定しない
'''


@app.route("/friend_request_list", methods=['GET', 'POST'])
def friend_request_list():
    # uid = session.get("uid")
    # if uid is None:
    #    return redirect("/login")
    receiver_id = request.form.get('id')

    # ログインユーザーの友達申請一覧を一覧を取得
    friend_request_list = dbConnect.getFriendReqList(receiver_id)

    return jsonify(friend_request_list)


'''
    return render_template(
        "/friend-request-list.html", friend_request_list=friend_request_list
    )
'''

"""
チャンネル
"""

# ホーム画面の表示


@app.route('/')
def home():
    user_id = session.get("user_id")
    if user_id is None:
        return redirect('/login')
    else:
        channel_type = 0
        channels = dbConnect.getChannels(user_id, channel_type)
    return render_template('home.html', channels=channels, user_id=user_id)

# グループ画面の表示


@app.route('/group')
def group():
    user_id = session.get("user_id")
    if user_id is None:
        return redirect('/login')
    else:
        channel_type = 1
        channels = dbConnect.getChannels(user_id, channel_type)
    return render_template('group.html', channels=channels, user_id=user_id)

# フレンド名による友達一覧の表示（グループ作成モーダル用）


def get_friends_list():
    user_id = session.get("user_id")
    friends_list = dbConnect.getFriendsList(user_id, user_id)
    # if not friends:
    #     # ユーザーが存在しない場合は空のfriends_infoを返す
    #     friends_info = {
    #         "friend_id": "",
    #         "user_name": "",
    #     }
    # else:
    #     friends_info = {
    #         "friend_id": friends["friend_id"],
    #         "user_name": friends["user_name"],
    #     }

    return jsonify(friends_list), 200  # JSONでユーザー情報を返却


'''
    return render_template(
        "group.html", friends_list=friend_List
    )
'''
# グループ作成


@app.route("/group_create", methods=["POST"])
def create_group():
    user_id = session.get("user_id")
    # if user_id is None:
    #     return redirect("/login")

    data = request.json
    newChannelName = data.get("newChannelName")

    channel = dbConnect.getChannelByName(newChannelName)
    if channel == None:
        newChannelDescription = data.get("newChannelDescription")
        newChannelType = "1"
        dbConnect.add_group_Channel(
            newChannelName, newChannelDescription, newChannelType
        )
        channel_id = data.get("channel_id")
        adminUid = user_id
        adminRole = "0"
        dbConnect.add_group_Channel_adminUser(channel_id, adminUid, adminRole)
        memberRole = "1"
        friends = data.get("friends")
        for friend_id in friends:
            dbConnect.add_group_Channel_Users(
                channel_id, friend_id, memberRole)
        return redirect("/group")
    else:
        error = "既に同じ名前のチャンネルが存在しています"
        return render_template("error/error.html", error_message=error)

# Public画面の表示


@app.route('/public')
def public():
    user_id = session.get("user_id")
    if user_id is None:
        return redirect('/login')
    else:
        channel_type = 2
        channels = dbConnect.getChannels(user_id, channel_type)
    return render_template('public.html', channels=channels, user_id=user_id)


# チャンネルの追加
@app.route('/', methods=['POST'])
def add_channel():
    user_id = session.get('user_id')
    if user_id is None:
        return redirect('/login')
    channel_name = request.form.get('channelTitle')
    channel = dbConnect.getChannelByName(channel_name)
    if channel == None:
        channel_description = request.form.get('channelDescription')
        dbConnect.addChannel(user_id, channel_name, channel_description)
        return redirect('/')
    else:
        error = '既に同じ名前のチャンネルが存在しています'
        return render_template('error/error.html', error_message=error)


# チャンネルの更新
@app.route('/update_channel', methods=['POST'])
def update_channel():
    user_id = session.get("user_id")
    if user_id is None:
        return redirect('/login')

    channel_id = request.form.get('channel_id')
    channel_name = request.form.get('channelTitle')
    channel_description = request.form.get('channelDescription')

    dbConnect.updateChannel(user_id, channel_name,
                            channel_description, channel_id)
    return redirect(f'/detail/{channel_id}')


# チャンネルの削除
@app.route('/delete/<channel_id>')
def delete_channel(channel_id):
    user_id = session.get("user_id")
    if user_id is None:
        return redirect('/login')
    else:
        channel = dbConnect.getChannelById(channel_id)
        if channel["user_id"] != user_id:
            flash('チャンネルは作成者のみ削除可能です')
            return redirect('/')
        else:
            dbConnect.deleteChannel(channel_id)
            channels = dbConnect.getChannelAll()
            return redirect('/')


# チャンネル詳細ページの表示
@app.route('/detail/<channel_id>')
def detail(channel_id):
    user_id = session.get("user_id")
    if user_id is None:
        return redirect('/login')

    channel = dbConnect.getChannelById(channel_id)
    messages = dbConnect.getMessageAll(channel_id)

    return render_template('detail.html', messages=messages, channel=channel, user_id=user_id)


"""
メッセージ
"""
# メッセージの投稿


@app.route('/message', methods=['POST'])
def add_message():
    user_id = session.get("user_id")
    if user_id is None:
        return redirect('/login')

    message = request.form.get('message')
    channel_id = request.form.get('channel_id')

    if message:
        dbConnect.createMessage(user_id, channel_id, message)

    return redirect(f'/detail/{channel_id}')


# メッセージの削除
@app.route('/delete_message', methods=['POST'])
def delete_message():
    user_id = session.get("user_id")
    if user_id is None:
        return redirect('/login')

    message_id = request.form.get('message_id')
    channel_id = request.form.get('channel_id')

    if message_id:
        dbConnect.deleteMessage(message_id)

    return redirect(f'/detail/{channel_id}')


"""
エラーハンドリング
"""


@app.errorhandler(404)
def show_error404(error):
    return render_template('error/404.html'), 404


@app.errorhandler(500)
def show_error500(error):
    return render_template('error/500.html'), 500


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
