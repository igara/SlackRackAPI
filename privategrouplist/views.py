# coding: UTF-8
from django.core import serializers
from django.http import HttpResponse, HttpResponseNotFound
from django.http.response import JsonResponse
from privategrouplist.models import PrivateGroup
from privategrouplist.models import Info

def get_group_list_action(request):
    """
        プライベートグループ情報表示のアクション
            return JsonResponse({"message":message})
            存在するプライベートグループをパラメータ指定された場合
            プライベートグループのメッセージがJsonで表示される
    """

    message = []
    group_info_id = PrivateGroup.objects.values('id').get(group_name__exact = request.GET['privategroup'])['id']

    for groups in Info.objects.all().filter(group_id = group_info_id).order_by('message_time_stamp').values():
        message.append({"user":groups['message_user'], "text":groups['message_text'], "ts":groups['message_time_stamp']})

    return JsonResponse({"message":message})
