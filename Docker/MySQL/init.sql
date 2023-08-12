
DROP DATABASE chatapp;
DROP USER 'testuser';

CREATE USER 'testuser' IDENTIFIED BY 'testuser';
CREATE DATABASE chatapp;
USE chatapp
GRANT ALL PRIVILEGES ON chatapp.* TO 'testuser';

CREATE TABLE users (
  id varchar(255) PRIMARY KEY,
  user_name varchar(255) NOT NULL,
  email varchar(255) UNIQUE NOT NULL,
  password varchar(255) NOT NULL
);  

INSERT INTO users (id, user_name, email, password)
VALUES
  ('1', 'ユーザー1', 'user1@example.com', 'password1'),
  ('2', 'ユーザー2', 'user2@example.com', 'password2'),
  ('3', 'ユーザー3', 'user3@example.com', 'password3'),
  ('4', 'ユーザー4', 'user4@example.com', 'password4');

CREATE TABLE friends (
  user_id varchar(255) NOT NULL,
  friend_id varchar(255) NOT NULL,
  PRIMARY KEY (user_id, friend_id),
  FOREIGN KEY (user_id) REFERENCES users (id),
  FOREIGN KEY (friend_id) REFERENCES users (id)
);

INSERT INTO friends (user_id, friend_id)
VALUES
  ('1', '2'),
  ('1', '3'),
  ('2', '4');

CREATE TABLE friend_requests (
  sender_id varchar(255) NOT NULL,
  receiver_id varchar(255) NOT NULL,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (sender_id, receiver_id),
  FOREIGN KEY (sender_id) REFERENCES users (id),
  FOREIGN KEY (receiver_id) REFERENCES users (id)
);

INSERT INTO friend_requests (sender_id, receiver_id)
VALUES
  ('3', '1'),
  ('4', '1');

CREATE TABLE channels (
  id INT NOT NULL AUTO_INCREMENT,
  channel_name varchar(255),
  abstract TEXT,
  type INT NOT NULL, -- 0: DM, 1: グループ, 2: Public
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id)
);

INSERT INTO channels (channel_name, abstract, type)
VALUES
  ('プライベートチャット', 'ユーザー1とユーザー2のプライベートチャット', 0),
  ('グループチャット', 'ユーザー1、ユーザー2、ユーザー3のグループチャット', 1),
  ('オープンチャンネル', 'オープンなチャンネル', 2);

CREATE TABLE channel_users (
  channel_id INT NOT NULL,
  user_id varchar(255) NOT NULL,
  role INT NOT NULL, -- 0: 管理者, 1: 一般, 2: ゲスト
  PRIMARY KEY (channel_id, user_id),
  FOREIGN KEY (channel_id) REFERENCES channels (id),
  FOREIGN KEY (user_id) REFERENCES users (id)
);

INSERT INTO channel_users (channel_id, user_id, role)
VALUES
  (1, '1', 0),
  (1, '2', 1),
  (2, '1', 0),
  (2, '2', 1),
  (2, '3', 1),
  (3, '1', 0),
  (3, '2', 1),
  (3, '3', 1);

CREATE TABLE messages (
  id INT NOT NULL AUTO_INCREMENT,
  channel_id INT NOT NULL,
  user_id varchar(255) NOT NULL,
  content TEXT NOT NULL,
  type INT NOT NULL, -- 0: channel_message, 1: note_message
  PRIMARY KEY (id),
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (channel_id) REFERENCES channels (id) ON DELETE CASCADE,
  FOREIGN KEY (user_id) REFERENCES users (id)
);

INSERT INTO messages (channel_id, user_id, content, type)
VALUES
  (1, '1', 'ユーザー1からのメッセージ', 0),
  (1, '2', 'ユーザー2からのメッセージ', 0),
  (1, '1', 'ユーザー1からのメッセージ2', 0),
  (2, '1', 'グループチャットでのメッセージ', 0),
  (2, '2', 'グループチャットでのメッセージ2', 0),
  (2, '3', 'グループチャットでのメッセージ3', 0),
  (3, '1', 'オープンチャンネルでのメッセージ', 0),
  (3, '2', 'オープンチャンネルでのメッセージ2', 0),
  (1, '1', 'ユーザー1からのメッセージ', 1),
  (1, '2', 'ユーザー2からのメッセージ', 1),
  (1, '1', 'ユーザー1からのメッセージ2', 1),
  (2, '1', 'グループチャットでのメッセージ', 1),
  (2, '2', 'グループチャットでのメッセージ2', 1),
  (2, '3', 'グループチャットでのメッセージ3', 1),
  (3, '1', 'オープンチャンネルでのメッセージ', 1),
  (3, '2', 'オープンチャンネルでのメッセージ2', 1);
