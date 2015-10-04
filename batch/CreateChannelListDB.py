#coding:utf-8
import json, urllib2, sqlite3
import const.const


class CreateChannelListDB:
    """
    Slackからチャンネル情報を取得するのDB作成
    """

    def get_channel_list(self):
        """
        Slackからチャンネル情報を取得するための関数
            return channel_id, channel_name
            チャンネルID, チャンネル名前
        """

        # チャンネルを取得するためのAPI
        url = 'https://slack.com/api/channels.list?token=' + const.const.TOKEN
        channels = None
        channel_name = []
        channel_id = []
        channel_topic_value = []
        
        try:
            # APIのJSONの情報をパースする
            r = urllib2.urlopen(url)
            root = json.loads(r.read())
            channels = root['channels']
            for channel in channels:
                # APIからチャンネルの名前とIDを取得する
                channel_name.append(channel['name'].decode('utf-8'))
                channel_id.append(channel['id'].decode('utf-8'))

        finally:
            r.close()
        return channel_id, channel_name
        
if __name__ == "__main__":
    # 自クラスの関数を呼びだす
    c = CreateChannelListDB()
    array = c.get_channel_list()

    # APIの情報をDBに入れる操作を行う
    insert_sql = u"insert into channelist_channel values (?, ?, ?)"
    select_sql = u"select channel_id from channelist_channel"
    conn = sqlite3.connect('db.sqlite3')
    cur = conn.cursor()
    cur.execute(select_sql)
    db_data = []
    for var in cur:
        db_data.append(var[0])
    
    miss_matched_list = [get_id for get_id in array[0] if not get_id in db_data]

    for miss_matched in miss_matched_list:
        cur.execute(insert_sql, (None, miss_matched, array[1][array[0].index(miss_matched)]))

    conn.commit()