#coding:utf-8
import json, urllib2, sqlite3
import const.const


class CreatePrivateGroupListDB:
    """
    Slackからプライベートグループ情報を取得するためのDB作成
    """

    def get_private_group_list(self):
        """
        Slackからチャンネル情報を取得するための関数
            return group_id, group_name
            チャンネルID, チャンネル名前
        """

        # プライベートグループを取得するためのAPI
        url = 'https://slack.com/api/groups.list?token=' + const.const.TOKEN
        groups = None
        group_name = []
        group_id = []
        group_topic_value = []
        
        try:
            # APIのJSONの情報をパースする
            r = urllib2.urlopen(url)
            root = json.loads(r.read())
            groups = root['groups']
            for group in groups:
                # APIからチャンネルの名前とIDを取得する
                group_name.append(group['name'].decode('utf-8'))
                group_id.append(group['id'].decode('utf-8'))
                #channel_topic_value.append(str(channel['topic']['value']).decode('ascii'))
        finally:
            r.close()
        return group_id, group_name
        
if __name__ == "__main__":
    # 自クラスの関数を呼びだす
    c = CreatePrivateGroupListDB()
    array = c.get_private_group_list()

    # APIの情報をDBに入れる操作を行う
    insert_sql = u"insert into privategrouplist_privategroup values (?, ?, ?)"
    select_sql = u"select group_id from privategrouplist_privategroup"
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