####SlackRackとは
Slackのメッセージを蓄積したものを見ることを目的にしたアプリケーション


####動作環境
Cloud9
Python2,3のDjangoで動作することを確認

####アプリケーションの使い方

クローン後
const.pyにSlackの秘密鍵等を貼る

DBの作成
コマンド
python manage.py syncdb
自動でDBが作成される

batchフォルダのバッチをcreateから実施を行う。
update batchでインサートが行われる

サーバ起動
python manage.py runserver $IP

URLの指定
slackrackフォルダのurls.pyが遷移できるURLパターンになる
http://localhost/slack/channelist/
チャンネル一覧がそれぞれhrefによるリンクが表示される
リンクから遷移することでチャンネルの情報を見ることができる

↓はCloud9公式の説明
     ,-----.,--.                  ,--. ,---.   ,--.,------.  ,------.
    '  .--./|  | ,---. ,--.,--. ,-|  || o   \  |  ||  .-.  \ |  .---'
    |  |    |  || .-. ||  ||  |' .-. |`..'  |  |  ||  |  \  :|  `--,
    '  '--'\|  |' '-' ''  ''  '\ `-' | .'  /   |  ||  '--'  /|  `---.
     `-----'`--' `---'  `----'  `---'  `--'    `--'`-------' `------'
    -----------------------------------------------------------------


Welcome to your Django project on Cloud9 IDE!

Your Django project is already fully setup. Just click the "Run" button to start
the application. On first run you will be asked to create an admin user. You can
access your application from 'https://localhost/' and the admin page from
'https://localhost/admin'.

## Starting from the Terminal

In case you want to run your Django application from the terminal just run:

1) Run syncdb command to sync models to database and create Django's default superuser and auth system

    $ python manage.py syncdb

2) Run Django

    $ python manage.py runserver $IP:$PORT

## Support & Documentation

Django docs can be found at https://www.djangoproject.com/

You may also want to follow the Django tutorial to create your first application:
https://docs.djangoproject.com/en/1.7/intro/tutorial01/

Visit http://docs.c9.io for support, or to learn more about using Cloud9 IDE.
To watch some training videos, visit http://www.youtube.com/user/c9ide
