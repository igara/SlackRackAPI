# coding: UTF-8
from django.core import serializers
from django.http import HttpResponse, HttpResponseNotFound
from django.template import loader, RequestContext
from django.http.response import JsonResponse
from channelist.models import Channel
from channelist.models import Info
from userlist.models import User
from django.core.exceptions import ObjectDoesNotExist
import const.const
import json, urllib2, sqlite3


def get_channel_list_action(request):
    """
        チャンネル情報表示のアクション
            return HttpResponse(template.render(contexts))
            パラメータ指定がない場合チャンネルリストが表示される

            return JsonResponse({"message":message})
            存在するチャンネルをパラメータ指定された場合
            チャンネルのメッセージがJsonで表示される
    """

    if not request.GET:

        channel_name = []
        for channel_names in Channel.objects.values('channel_name'):
            channel_name.append(channel_names['channel_name'])

        contexts = RequestContext(request, {
            'title' : 'channel_list',
            'channel_name' : channel_name,
        })
        template = loader.get_template('index.html')
        return HttpResponse(template.render(contexts))

    members = []
    message = []

    # ユーザを取得するためのAPI
    url = 'https://slack.com/api/users.list?token=' + const.const.TOKEN
    try:
        # APIのJSONの情報をパースする
        r = urllib2.urlopen(url)
        root = json.loads(r.read())
        members = root['members']

    finally:
        r.close()

    channel_info_id = Channel.objects.values('id').get(channel_name__exact = request.GET['channel'])['id']

    for channels in Info.objects.all().filter(channel_id = channel_info_id).order_by('message_time_stamp').values():
        try:
            user_info = User.objects.all().values().get(user_id__exact = channels['message_user'])
            message.append({"user_id":channels['message_user'],
                            "profile":{
                                "image_24":get_profile_image(members, channels['message_user'])[0],
                                "image_32":get_profile_image(members, channels['message_user'])[1],
                                "image_48":get_profile_image(members, channels['message_user'])[2],
                                "image_72":get_profile_image(members, channels['message_user'])[3],
                                "image_192":get_profile_image(members, channels['message_user'])[4],
                                "image_original":get_profile_image(members, channels['message_user'])[5]},
                            "user_name":user_info['user_name'],
                            "text":channels['message_text'],
                            "ts":channels['message_time_stamp']})
        except ObjectDoesNotExist:
            message.append({"user_id":channels['message_user'],
                            "text":channels['message_text'],
                            "ts":channels['message_time_stamp']})
    return JsonResponse({"message":message})

def get_channel_list_json_action(request):
    """
        チャンネルリスト情報表示のアクション
            return JsonResponse({"channel_name":channel_name})
            存在するチャンネルをパラメータ指定された場合
            チャンネルの一覧がJsonで表示される
    """
    channel_name = []
    for channel_names in Channel.objects.values('channel_name'):
        channel_name.append(channel_names['channel_name'])

    return JsonResponse({"channel_name":channel_name})


def get_profile_image(apiJson, userId):
    """
        ユーザのプロフィール画像取得
        公式から直接とるようにする予定
    """
    for member in apiJson:
        if member['id'] == userId:
            return (member['profile']['image_24'],
                    member['profile']['image_32'],
                    member['profile']['image_48'],
                    member['profile']['image_72'],
                    member['profile']['image_192'],
                    member['profile']['image_original'])
