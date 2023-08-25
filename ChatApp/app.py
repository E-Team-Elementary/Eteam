from flask import (
    Flask,
    request,
    redirect,
    render_template,
    session,
    flash,
    abort,
    jsonify,
    make_response,
    json,
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
            UserName = str(user_name)
            session["user_id"] = UserId
            session["user_name"] = UserName
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
                session["user_name"] = user["user_name"]
                return redirect("/")
    return redirect("/login")


# ログアウト
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


"""
フレンド
"""


# フレンド追加機能
@app.route("/search_user", methods=["POST"])
def search_user():
    user_id = session.get("user_id")
    if user_id is None:
        return redirect("/login")
    email = request.form.get("email")
    current_user_id = user_id
    user = dbConnect.getUserByEmail(email)

    if not user:
        response = make_response(json.dumps({"message": "ユーザーが見つかりませんでした。"}), 404)
        response.mimetype = "application/json"
        return response

    if current_user_id == user["id"]:
        response = jsonify({"message": "自分のメールアドレスは検索できません。"})
        response.status_code = 400
        return response

    is_friend = dbConnect.checkFriend(user["id"], current_user_id)
    if is_friend["is_friend"] == "Yes":
        response = jsonify({"message": "このユーザーは既にフレンドです。"})
        response.status_code = 400
        return response

    user_info = {
        "user_id": user["id"],
        "user_name": user["user_name"],
        "email": user["email"],
    }
    return jsonify(user_info), 200


# フレンド申請を作成する
@app.route("/friend_request", methods=["POST"])
def friend_request():
    user_id = session.get("user_id")
    if user_id is None:
        return redirect("/login")
    data = request.json
    sender_id = user_id
    receiver_id = data.get("receiver_id")
    if sender_id is None or receiver_id is None:
        return (
            jsonify(
                {"error": "Invalid request data. Missing sender_id or receiver_id."}
            ),
            400,
        )
    result = dbConnect.createFriendRequest(sender_id, receiver_id)
    redirect_url = "/"
    response = jsonify({"redirect_url": redirect_url})
    response.headers["X-Redirect"] = redirect_url
    if result == "success":
        flash("OK:フレンド申請を送りました")
    elif result == "duplicate":
        flash("NG:既に申請済みです")
    elif result == "error":
        flash("OK:申請に失敗しました")
    return response


# ログインユーザーに対して、友達申請一覧を取得


@app.route("/friend_request")
def friend_request_list():
    user_id = session.get("user_id")
    if user_id is None:
        return redirect("/login")

    user_id = session.get("user_id")
    # ログインユーザーの友達申請一覧を一覧を取得
    request_list = dbConnect.getFriendReqList(user_id)

    # データをJSON形式に整形して返す
    result = []
    for request in request_list:
        request_data = {
            "sender_id": request["sender_id"],
            "sender_name": request["sender_name"],
            "created_at": request["created_at"].strftime("%Y-%m-%d %H:%M:%S"),
        }
        result.append(request_data)

    return jsonify(result), 200


# 友達申請承認・拒否処理
@app.route("/friend-response", methods=["POST"])
def friend_request_result():
    user_id = session.get("user_id")
    if user_id is None:
        return redirect("/login")

    data = request.json
    sender_id = data.get("sender_id")
    receiver_id = user_id
    response = data.get("response")

    dbConnect.deleteFriendRequest(sender_id, receiver_id)

    if response == "accept":
        channel_type = TYPE.FRIEND_CHAT
        channel_description = ""
        sender_data = dbConnect.getUserById(sender_id)
        receiver_data = dbConnect.getUserById(receiver_id)
        channel_name = sender_data["user_name"] + ":" + receiver_data["user_name"]
        role = TYPE.CHAT_ADMIN

        result = dbConnect.addFriendAndChannel(
            sender_id,
            receiver_id,
            channel_name,
            channel_description,
            channel_type,
            role,
        )

        if result == "success":
            flash("OK:フレンド申請を承認しました")
        elif result == "error":
            flash("NG:エラーが発生しました")

    elif response == "deny":
        flash("NG:フレンド申請を拒否しました")

    redirect_url = "/"
    response = jsonify({"redirect_url": redirect_url})
    response.headers["X-Redirect"] = redirect_url
    return response


"""
各画面の表示
"""


# ホーム画面(フレンド画面)の表示
@app.route("/")
def home():
    user_id = session.get("user_id")
    if user_id is None:
        return redirect("/login")
    else:
        user_name = session.get("user_name")
        channels = dbConnect.getChannels(user_id, TYPE.FRIEND_CHAT)
        friend_list = dbConnect.getFriendsList(user_id, user_id)
    return render_template(
        "home/home-base.html",
        channels=channels,
        user_id=user_id,
        user_name=user_name,
        friend_list=friend_list,
    )


# フレンド詳細ページの表示
@app.route("/friend/<channel_id>")
def detail_friend(channel_id):
    user_id = session.get("user_id")
    if user_id is None:
        return redirect("/login")

    user_name = session.get("user_name")
    channel = dbConnect.getChannelById(channel_id)
    messages = dbConnect.getMessageAll(channel_id, type=TYPE.CHAT_MESSAGE)
    notes = dbConnect.getMessageAll(channel_id, type=TYPE.NOTE_MESSAGE)
    channel_type = channel["type"]
    channels = dbConnect.getChannels(user_id, channel_type)

    # 友達一覧の取得
    friend_list = dbConnect.getFriendsList(user_id, user_id)

    return render_template(
        "home/home.html",
        messages=messages,
        channel=channel,
        user_id=user_id,
        user_name=user_name,
        channels=channels,
        friend_list=friend_list,
        notes=notes,
    )


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


# グループ詳細ページの表示
@app.route("/group/<channel_id>")
def detail_group(channel_id):
    user_id = session.get("user_id")
    if user_id is None:
        return redirect("/login")

    channel = dbConnect.getChannelById(channel_id)
    messages = dbConnect.getMessageAll(channel_id, type=TYPE.CHAT_MESSAGE)
    notes = dbConnect.getMessageAll(channel_id, type=TYPE.NOTE_MESSAGE)
    channel_type = TYPE.GROUP_CHAT
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
        notes=notes,
    )


# Public画面の表示
@app.route("/public")
def public():
    user_id = session.get("user_id")
    if user_id is None:
        return redirect("/login")
    else:
        channels = dbConnect.getChannels(user_id, TYPE.PUBLIC_CHAT)
    return render_template("home/public-base.html", channels=channels, user_id=user_id)


# パブリック詳細ページの表示
@app.route("/public/<channel_id>")
def detail_public(channel_id):
    user_id = session.get("user_id")
    if user_id is None:
        return redirect("/login")

    channel = dbConnect.getChannelById(channel_id)
    messages = dbConnect.getMessageAll(channel_id, type=TYPE.CHAT_MESSAGE)
    notes = dbConnect.getMessageAll(channel_id, type=TYPE.NOTE_MESSAGE)
    channel_type = channel["type"]
    channels = dbConnect.getChannels(user_id, channel_type)

    return render_template(
        "home/public.html",
        messages=messages,
        channel=channel,
        user_id=user_id,
        channels=channels,
        notes=notes,
    )


"""
トークルーム作成(フレンドとのチャットは承認した時点で作成される為、フレンドにコードあり)
"""


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
        return render_template("error/error.html", error_message=error)


# パブリックチャット作成
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


"""
トークルーム削除(フレンドは削除されない仕様)
"""


# Groupチャンネルの削除
@app.route("/delete_channel", methods=["POST"])
def delete_channel():
    user_id = session.get("user_id")
    if user_id is None:
        return redirect("/login")
    else:
        channel_id = request.form.get("channel_id")
        dbConnect.deleteChannel_group(channel_id)

        flash("OK:チャンネルを削除しました")
        return redirect(f"/group")


# publicチャンネルの削除
@app.route("/delete_channel_public", methods=["POST"])
def delete_channel_public():
    user_id = session.get("user_id")
    if user_id is None:
        return redirect("/login")
    else:
        channel_id = request.form.get("channel_id")
        dbConnect.deleteChannel_public(channel_id)

        flash("OK:チャンネルを削除しました")
        return redirect(f"/public")


"""
トークルーム情報更新
チャンネル名とチャンネル概要の更新
"""


# Groupチャンネルの更新
@app.route("/update_channel_group", methods=["POST"])
def update_channel_group():
    user_id = session.get("user_id")
    if user_id is None:
        return redirect("/login")

    channel_id = request.form.get("channel_id")
    channel_name = request.form.get("editName")
    channel_description = request.form.get("editDescription")

    dbConnect.updateChannel(channel_name, channel_description, channel_id)
    flash("OK:チャンネルを編集しました")
    return redirect(f"/group/{channel_id}")


# publicチャンネルの更新
@app.route("/update_channel_public", methods=["POST"])
def update_channel_public():
    user_id = session.get("user_id")
    if user_id is None:
        return redirect("/login")

    channel_id = request.form.get("channel_id")
    channel_name = request.form.get("editPublicName")
    channel_description = request.form.get("editDescription")

    dbConnect.updateChannel(channel_name, channel_description, channel_id)
    flash("OK:チャンネルを編集しました")
    return redirect("/public")


"""
メッセージ
"""
# メッセージの投稿


# フレンドとのメッセージ、ノートの送信
@app.route("/post_message_friend", methods=["POST"])
def add_message_friend():
    user_id = session.get("user_id")
    if user_id is None:
        return redirect("/login")

    message = request.form.get("message")
    channel_id = request.form.get("channel_id")
    # typeによってメッセージとノートの投稿を分けている
    type = request.form.get("message_type")

    dbConnect.createMessage(channel_id, user_id, message, type)

    return redirect(f"/friend/{channel_id}")


# グループでのメッセージ、ノートの送信
@app.route("/post_message", methods=["POST"])
def add_message():
    user_id = session.get("user_id")
    if user_id is None:
        return redirect("/login")

    message = request.form.get("message")
    channel_id = request.form.get("channel_id")
    type = request.form.get("message_type")

    dbConnect.createMessage(channel_id, user_id, message, type)

    return redirect(f"/group/{channel_id}")


# パブリックでのメッセージ、ノートの送信
@app.route("/post_message_public", methods=["POST"])
def add_message_public():
    user_id = session.get("user_id")
    if user_id is None:
        return redirect("/login")

    message = request.form.get("message")
    channel_id = request.form.get("channel_id")
    type = request.form.get("message_type")

    dbConnect.createMessage(channel_id, user_id, message, type)

    return redirect(f"/public/{channel_id}")


# メッセージの削除


# フレンドとのメッセージ、ノートの削除
@app.route("/delete_message_friend", methods=["POST"])
def delete_message_friend():
    user_id = session.get("user_id")
    if user_id is None:
        return redirect("/login")

    message_id = request.form.get("message_id")
    channel_id = request.form.get("channel_id")

    if message_id:
        dbConnect.deleteMessage(message_id)

    return redirect(f"/friend/{channel_id}")


# グループでのメッセージ、ノートの削除
@app.route("/delete_message", methods=["POST"])
def delete_message():
    user_id = session.get("user_id")
    if user_id is None:
        return redirect("/login")

    message_id = request.form.get("message_id")
    channel_id = request.form.get("channel_id")

    if message_id:
        dbConnect.deleteMessage(message_id)

    return redirect(f"/group/{channel_id}")


# パブリックでのメッセージ、ノートの削除
@app.route("/delete_message_public", methods=["POST"])
def delete_message_public():
    user_id = session.get("user_id")
    if user_id is None:
        return redirect("/login")

    message_id = request.form.get("message_id")
    channel_id = request.form.get("channel_id")

    if message_id:
        dbConnect.deleteMessage(message_id)

    return redirect(f"/public/{channel_id}")


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
