#coding:utf-8
import json, urllib2, sqlite3
import const.const

class UpdateChannelMessage:
    """
    Slackからのチャンネル情報をDBにいれる
    """

    def get_channel_message(self):
        """
        Slackからチャンネルからメッセージを取得するための関数
            return channel_message_user, channel_message_text, channel_message_ts, id
            ユーザ名, テキスト, タイムスタンプ, DBのキー値
        """

        url = 'https://slack.com/api/channels.history?count=1000&token=' + const.const.TOKEN +'&channel='
        messages = None
        channel_message_user = []
        channel_message_text = []
        channel_message_attachments_fallback = []
        channel_message_attachments_text = []
        channel_message_ts = []
        id = []

        select_sql = u"select id, channel_id from channelist_channel"
        conn = sqlite3.connect('db.sqlite3')
        cur = conn.cursor()
        cur.execute(select_sql)

        for var in cur:
            try:
                r = urllib2.urlopen(url + str(var[1]))
                root = json.loads(r.read())
                messages = root['messages']

                if messages:
                    for message in messages:
                        if not 'comment' in message:
                            if 'user' in message:
                                # APIからメッセージに対するユーザを取得する
                                channel_message_user.append(message['user'])
                            elif 'bot_id' in message:
                                # APIからメッセージに対するボットもユーザとして取得する
                                channel_message_user.append(message['bot_id'])
                            elif not 'bot_id' in message and not 'user' in message:
                                # APIからメッセージに対するボットでもユーザでもないものをユーザとして扱う
                                if 'username' in message:
                                    channel_message_user.append(message['username'])
                            if 'text' in message:
                                channel_message_text.append(message['text'])

                            if 'attachments' in message:
                                for attachment in message['attachments']:
                                    if 'fallback' in attachment:
                                        channel_message_attachments_fallback.append(attachment['fallback'])
                                    else:
                                        channel_message_attachments_fallback.append(None)
                                    if 'text' in attachment:
                                        channel_message_attachments_text.append(attachment['text'])
                                    else:
                                        channel_message_attachments_text.append(None)
                            else:
                                channel_message_attachments_fallback.append(None)
                                channel_message_attachments_text.append(None)

                            if 'ts' in message:
                                # APIからメッセージに対するタイムスタンプを取得する
                                channel_message_ts.append(message['ts'])

                            id.append(var[0])

            finally:
                r.close()

        return channel_message_user, channel_message_text, channel_message_attachments_fallback, channel_message_attachments_text,channel_message_ts, id

if __name__ == "__main__":
    c = UpdateChannelMessage()
    array = c.get_channel_message()
    select_sql = u"select id, message_time_stamp from channelist_info"
    conn = sqlite3.connect('db.sqlite3')
    cur = conn.cursor()
    cur.execute(select_sql)
    db_data = []
    # print array[0] # ユーザ
    # print array[1] # テキスト
    # print array[2] #
    # print array[3] #
    # print array[4] # ts
    # print array[5] # id


    for var in cur:
        db_data.append(var[1])

    miss_matched_list = [get_ts for get_ts in array[4] if not get_ts in db_data]

    print '---------------------------------'
    # user
    print 'APIのコメントしたユーザ数' + str(len(array[0]))
    # text
    print 'APIのコメント数' + str(len(array[1]))
    # ts
    print 'APIのタイムスタンプ数' + str(len(array[4]))

    print '---------------------------------'

    print '新規追加数' + str(len(miss_matched_list))

    insert_sql = u"insert into channelist_info (id, channel_id, message_user, message_text, attachments_fallback, attachments_text, message_time_stamp ) values (?, ?, ?, ?, ?, ?, ?)"
    # マッチしない物は追加処理を行う
    for miss_matched in miss_matched_list:
        # id, user, attachments_fallback, attachments_text, text, ts
        cur.execute(insert_sql, (None, array[5][array[4].index(miss_matched)], array[0][array[4].index(miss_matched)], array[1][array[4].index(miss_matched)], array[2][array[4].index(miss_matched)], array[3][array[4].index(miss_matched)], array[4][array[4].index(miss_matched)]))

    conn.commit()
