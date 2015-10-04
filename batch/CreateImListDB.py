#coding:utf-8
import json, urllib2, sqlite3
import const.const


class CreateImListDB:
    """
    Slackからダイレクトメッセージ情報を取得するためのDB作成
    """

    def get_im_list(self):
        """
        Slackからダイレクトメッセージ情報を取得するための関数
            return im_id, im_user
            チャンネルID, チャンネル名前
        """

        # プライベートグループを取得するためのAPI
        url = 'https://slack.com/api/im.list?token=' + const.const.TOKEN
        ims = None
        im_user = []
        im_id = []
        im_topic_value = []
        
        try:
            # APIのJSONの情報をパースする
            r = urllib2.urlopen(url)
            root = json.loads(r.read())
            ims = root['ims']
            for im in ims:
                # APIからチャンネルの名前とIDを取得する
                im_user.append(im['user'].decode('utf-8'))
                im_id.append(im['id'].decode('utf-8'))

        finally:
            r.close()
        return im_id, im_user
        
if __name__ == "__main__":
    # 自クラスの関数を呼びだす
    c = CreateImListDB()
    array = c.get_im_list()

    # APIの情報をDBに入れる操作を行う
    insert_sql = u"insert into imlist_im values (?, ?, ?)"
    select_sql = u"select im_id from imlist_im"
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