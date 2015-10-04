#coding:utf-8
import json, urllib2, sqlite3
import const.const

class UpdatePrivateGroupMessage:
    """
    Slackからのプライベートグループ情報をDBにいれる
    """

    def get_private_group_message(self):
        """
        Slackからチャンネルからメッセージを取得するための関数
            return group_message_user, group_message_text, group_message_ts, id
            ユーザ名, テキスト, タイムスタンプ, DBのキー値
        """

        url = 'https://slack.com/api/groups.history?count=1000&token=' + const.const.TOKEN +'&channel='
        messages = None
        group_message_user = []
        group_message_text = []
        group_message_ts = []
        id = []
        
        select_sql = u"select id, group_id from privategrouplist_privategroup"
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
                            if 'user' in message:
                                # APIからメッセージに対するユーザを取得する
                                group_message_user.append(message['user'])
                            if 'bot_id' in message:
                                # APIからメッセージに対するボットもユーザとして取得する
                                group_message_user.append(message['bot_id'])
                            if not 'bot_id' in message and not 'user' in message:
                                # APIからメッセージに対するボットでもユーザでもないものをユーザとして扱う
                                if 'username' in message:
                                    group_message_user.append(message['username'])
                            if 'text' in message:
                                # APIからメッセージに対するメッセージ内容を取得する
                                group_message_text.append(message['text'])
                            if 'ts' in message:
                                # APIからメッセージに対するタイムスタンプを取得する
                                group_message_ts.append(message['ts'])

                            id.append(var[0])

            finally:
                r.close()
                
        return group_message_user, group_message_text, group_message_ts, id
        
if __name__ == "__main__":
    c = UpdatePrivateGroupMessage()
    array = c.get_private_group_message()
    insert_sql = u"insert into privategrouplist_info values (?, ?, ?, ?, ?)"
    select_sql = u"select id, message_time_stamp from privategrouplist_info"
    conn = sqlite3.connect('db.sqlite3')
    cur = conn.cursor()
    cur.execute(select_sql)
    db_data = []
    for var in cur:
        db_data.append(var[1])
    
    miss_matched_list = [get_ts for get_ts in array[2] if not get_ts in db_data]

    print '---------------------------------'
    # user
    print 'APIのコメントしたユーザ数' + str(len(array[0]))#2
    # text
    print 'APIのコメント数' + str(len(array[1]))#1
    # ts
    print 'APIのタイムスタンプ数' + str(len(array[2]))#3

    print '---------------------------------'
    
    print '新規追加数' + str(len(miss_matched_list))

    # マッチしない物は追加処理を行う
    for miss_matched in miss_matched_list:
        # message, message, user, ts,id
        cur.execute(insert_sql, (None, array[1][array[2].index(miss_matched)], array[0][array[2].index(miss_matched)], miss_matched, array[3][array[2].index(miss_matched)]))

    conn.commit()
