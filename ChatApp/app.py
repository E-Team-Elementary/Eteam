from flask import (
    Flask,
    request,
    redirect,
    render_template,
    session,
    flash,
    abort,
    jsonify,
)
from datetime import timedelta
import hashlib
import uuid
import re

from models import dbConnect
from util.TYPE import TYPE

app = Flask(__name__)
app.secret_key = uuid.uuid4().hex
app.permanent_session_lifetime = timedelta(days=30)

"""
ユーザー認証 
"""
# サインアップページの表示


@app.route("/signup")
def signup():
    return render_template("registration/signup.html")


# サインアップ処理
@app.route("/signup", methods=["POST"])
def userSignup():
    user_name = request.form.get("name")
    email = request.form.get("email")
    password1 = request.form.get("password1")
    password2 = request.form.get("password2")

    pattern = "^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"

    if user_name == "" or email == "" or password1 == "" or password2 == "":
        flash("空のフォームがあるようです")
    elif password1 != password2:
        flash("二つのパスワードの値が違っています")
    elif re.match(pattern, email) is None:
        flash("正しいメールアドレスの形式ではありません")
    else:
        user_id = uuid.uuid4()
        password = hashlib.sha256(password1.encode("utf-8")).hexdigest()
        DBuser = dbConnect.getUserByEmail(email)

        if DBuser != None:
            flash("既に登録されているようです")
        else:
            dbConnect.createUser(user_id, user_name, email, password)
            UserId = str(user_id)
            session["user_id"] = UserId
            return redirect("/")
    return redirect("/signup")


# ログインページの表示
@app.route("/login")
def login():
    return render_template("registration/login.html")


# ログイン処理
@app.route("/login", methods=["POST"])
def userLogin():
    email = request.form.get("email")
    password = request.form.get("password")

    if email == "" or password == "":
        flash("空のフォームがあるようです")
    else:
        user = dbConnect.getUserByEmail(email)
        if user is None:
            flash("このユーザーは存在しません")
        else:
            hashPassword = hashlib.sha256(password.encode("utf-8")).hexdigest()
            if hashPassword != user["password"]:
                flash("パスワードが間違っています！")
            else:
                session["user_id"] = user["id"]
                return redirect("/")
    return redirect("/login")


# ログアウト
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


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
@app.route("/search_user", methods=["POST"])
def search_user():
    # user_id = session.get("user_id")
    # if user_id is None:
    #     return redirect('/login')
    email = request.form.get("email")
    user = dbConnect.getUserByEmail(email)
    if not user:
        # ユーザーが存在しない場合は空のuser_infoを返す
        user_info = {
            "user_id": "",
            "user_name": "",
            "email": "",
        }
    else:
        user_info = {
            "user_id": user["id"],
            "user_name": user["user_name"],
            "email": user["email"],
        }
    return jsonify(user_info), 200  # JSONでユーザー情報を返却


# フレンド申請を作成する
@app.route("/friend_request", methods=["POST"])
def friend_request():
    # user_id = session.get("user_id")
    # if user_id is None:
    #     return redirect('/login')
    data = request.json
    sender_id = data.get("sender_id")
    receiver_id = data.get("receiver_id")
    if sender_id is None or receiver_id is None:
        return (
            jsonify(
                {"error": "Invalid request data. Missing sender_id or receiver_id."}
            ),
            400,
        )
    result = dbConnect.createFriendRequest(sender_id, receiver_id)

    if result == "success":
        return jsonify({"message": "フレンド申請を送りました"}), 200
    elif result == "duplicate":
        return jsonify({"message": "既に申請済みです"}), 422
    elif result == "error":
        return jsonify({"message": "申請に失敗しました"}), 422


# ログインユーザーに対して、友達申請一覧を取得し、友達申請一覧画面(仮)に遷移
"""
 todo:
 フレンド一覧を取得する時、本来はGetメソッドを指定する予定だが、テスト用にPOSTも指定している
 セッション周りのコメントを外す、POSTを指定しない
"""


@app.route("/friend_request_list", methods=["GET", "POST"])
def friend_request_list():
    # uid = session.get("uid")
    # if uid is None:
    #    return redirect("/login")
    receiver_id = request.form.get("id")

    # ログインユーザーの友達申請一覧を一覧を取得
    friend_request_list = dbConnect.getFriendReqList(receiver_id)

    return jsonify(friend_request_list)


"""
    return render_template(
        "/friend-request-list.html", friend_request_list=friend_request_list
    )
"""


# 友達申請承認・拒否処理
@app.route("/friend_request_result", methods=["POST"])
def friend_request_result():
    # uid = session.get("uid")
    # if uid is None:
    #    return redirect("/login")
    receiver_id = request.form.get("user_id")
    sender_id = request.form.get("sender_id")
    result = request.form.get("result")

    # 申請が許可された時
    if result == 0:
        # friendsテーブルにデータを追加
        # dbConnect.addFriend(receiver_id, sender_id)

        receiver_data = dbConnect.getUserById(receiver_id)
        sender_data = dbConnect.getUserById(sender_id)

        channelName = receiver_data["name"] + sender_data["name"]

        # 個人チャットを作成
        # dbConnect.addChannelGetId()

        return str(channelName)
    else:
        print("")


"""
チャンネル
"""

# ホーム画面の表示


@app.route("/")
def home():
    user_id = session.get("user_id")
    if user_id is None:
        return redirect("/login")
    else:
        channel_type = 0
        channels = dbConnect.getChannels(user_id, channel_type)
    return render_template("home/home-base.html", channels=channels, user_id=user_id)


# グループ画面の表示


@app.route("/group")
def group():
    user_id = session.get("user_id")
    if user_id is None:
        return redirect("/login")
    else:
        # グループチャンネルの一覧を取得
        channels = dbConnect.getChannels(user_id, TYPE.GROUP_CHAT)
        # 友達一覧の取得
        friend_list = dbConnect.getFriendsList(user_id, user_id)

    return render_template(
        "home/groups-base.html",
        channels=channels,
        user_id=user_id,
        friend_list=friend_list,
    )


# グループ作成


@app.route("/group_create", methods=["POST"])
def create_group():
    user_id = session.get("user_id")
    if user_id is None:
        return redirect("/login")

    channel_name = request.form.get("channelTitle")

    channel = dbConnect.getChannelByName(channel_name)
    if channel == None:
        channel_description = request.form.get("channelDescription")

        # チャンネル追加処理
        channel_id = dbConnect.addChannelGetId(
            channel_name, channel_description, TYPE.GROUP_CHAT
        )

        # チャンネル管理者登録
        dbConnect.addChannelUser(channel_id[0]["current_id"], user_id, TYPE.CHAT_ADMIN)

        # チャンネルメンバー登録
        friends = request.form.getlist("friends")
        for friend_id in friends:
            dbConnect.addChannelUser(
                channel_id[0]["current_id"], friend_id, TYPE.CHAT_MEMBER
            )
        return redirect("/group")
    else:
        error = "既に同じ名前のチャンネルが存在しています"
        # return render_template("error/error.html", error_message=error)
        return error


# Public画面の表示


@app.route("/public")
def public():
    user_id = session.get("user_id")
    if user_id is None:
        return redirect("/login")
    else:
        channels = dbConnect.getChannels(user_id, TYPE.PUBLIC_CHAT)
    return render_template("home/public-base.html", channels=channels, user_id=user_id)


# チャンネルの追加


@app.route("/public", methods=["POST"])
def add_channel():
    user_id = session.get("user_id")
    if user_id is None:
        return redirect("/login")

    channel_name = request.form.get("inputPublicName")
    channel = dbConnect.getChannelByName(channel_name)
    if channel == None:
        channel_description = request.form.get("publicDescription")

        # チャンネル追加処理
        channel_id = dbConnect.addChannelGetId(
            channel_name, channel_description, TYPE.PUBLIC_CHAT
        )
        # チャンネルユーザー登録処理
        dbConnect.addChannelUser(channel_id[0]["current_id"], user_id, TYPE.CHAT_ADMIN)

        return redirect("/public")

    else:
        error = "既に同じ名前のチャンネルが存在しています"
        return render_template("error/error.html", error_message=error)


# チャンネルの更新
@app.route("/update_channel", methods=["POST"])
def update_channel():
    user_id = session.get("user_id")
    if user_id is None:
        return redirect("/login")

    channel_id = request.form.get("channel_id")
    channel_name = request.form.get("channelTitle")
    channel_description = request.form.get("channelDescription")

    dbConnect.updateChannel(user_id, channel_name, channel_description, channel_id)
    return redirect(f"/detail/{channel_id}")


# チャンネルの削除
@app.route("/delete/<channel_id>")
def delete_channel(channel_id):
    user_id = session.get("user_id")
    if user_id is None:
        return redirect("/login")
    else:
        channel = dbConnect.getChannelById(channel_id)
        if channel["user_id"] != user_id:
            flash("チャンネルは作成者のみ削除可能です")
            return redirect("/")
        else:
            dbConnect.deleteChannel(channel_id)
            channels = dbConnect.getChannelAll()
            return redirect("/")


# チャンネル詳細ページの表示
@app.route("/friend/<channel_id>")
def detail_friend(channel_id):
    user_id = session.get("user_id")
    if user_id is None:
        return redirect("/login")

    channel = dbConnect.getChannelById(channel_id)
    messages = dbConnect.getMessageAll(channel_id)
    channel_type = channel["type"]
    channels = dbConnect.getChannels(user_id, channel_type)

    return render_template(
        "home/home.html",
        messages=messages,
        channel=channel,
        user_id=user_id,
        channels=channels,
    )


@app.route("/group/<channel_id>")
def detail_group(channel_id):
    user_id = session.get("user_id")
    if user_id is None:
        return redirect("/login")

    channel = dbConnect.getChannelById(channel_id)
    messages = dbConnect.getMessageAll(channel_id)
    channel_type = channel["type"]
    channels = dbConnect.getChannels(user_id, channel_type)

    # 友達一覧の取得
    friend_list = dbConnect.getFriendsList(user_id, user_id)

    return render_template(
        "home/groups.html",
        messages=messages,
        channel=channel,
        user_id=user_id,
        channels=channels,
        friend_list=friend_list,
    )


@app.route("/public/<channel_id>")
def detail_public(channel_id):
    user_id = session.get("user_id")
    if user_id is None:
        return redirect("/login")

    channel = dbConnect.getChannelById(channel_id)
    messages = dbConnect.getMessageAll(channel_id)
    channel_type = channel["type"]
    channels = dbConnect.getChannels(user_id, channel_type)

    return render_template(
        "home/public.html",
        messages=messages,
        channel=channel,
        user_id=user_id,
        channels=channels,
    )


"""
メッセージ
"""
# メッセージの投稿


# chat部分で投稿された内容をmessagesテーブルに挿入
"""
 todo:
 セッション周りのコメントを外す、リダイレクト先を指定する
"""


@app.route("/post_message", methods=["POST"])
def add_message():
    user_id = session.get("user_id")
    if user_id is None:
        return redirect("/login")
    # user_id = request.form.get("user_id")

    message = request.form.get("message")
    channel_id = request.form.get("channel_id")
    type = request.form.get("message_type")

    # messageとnoteで処理を分ける
    if type == 0:
        dbConnect.createMessage(user_id, channel_id, message, TYPE.CHAT_MESSAGE)
    else:
        dbConnect.createMessage(user_id, channel_id, message, TYPE.NOTE_MESSAGE)

    return redirect(f"/detail/{channel_id}")


# メッセージの削除
@app.route("/delete_message", methods=["POST"])
def delete_message():
    user_id = session.get("user_id")
    if user_id is None:
        return redirect("/login")

    message_id = request.form.get("message_id")
    channel_id = request.form.get("channel_id")

    if message_id:
        dbConnect.deleteMessage(message_id)

    return redirect(f"/detail/{channel_id}")


"""
エラーハンドリング
"""


@app.errorhandler(404)
def show_error404(error):
    return render_template("error/404.html"), 404


@app.errorhandler(500)
def show_error500(error):
    return render_template("error/500.html"), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
