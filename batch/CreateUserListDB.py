#coding:utf-8
import json, urllib2, sqlite3
import const.const


class CreateImListDB:
    """
    Slackからユーザ情報を取得するためのDB作成
    """

    def get_user_list(self):
        """
        Slackからユーザ情報を取得するための関数
            return members_id, members_user
            ユーザID, ユーザ名前
        """

        # ユーザを取得するためのAPI
        url = 'https://slack.com/api/users.list?token=' + const.const.TOKEN
        users = None
        members_user = []
        members_id = []
        
        try:
            # APIのJSONの情報をパースする
            r = urllib2.urlopen(url)
            root = json.loads(r.read())
            users = root['members']
            for user in users:
                # APIからチャンネルの名前とIDを取得する
                members_user.append(user['name'].decode('utf-8'))
                members_id.append(user['id'].decode('utf-8'))
                #channel_topic_value.append(str(channel['topic']['value']).decode('ascii'))
        finally:
            r.close()
        return members_id, members_user
        
if __name__ == "__main__":
    # 自クラスの関数を呼びだす
    c = CreateImListDB()
    array = c.get_user_list()

    # APIの情報をDBに入れる操作を行う
    insert_sql = u"insert into userlist_user values (?, ?, ?)"
    #delete from sqlite_sequence where name='userlist_user';
    #delete from sqlite_sequence where name='userlist_info';
    select_sql = u"select user_id from userlist_user"
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