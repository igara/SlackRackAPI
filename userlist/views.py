# coding: UTF-8
from django.core import serializers
from django.http import HttpResponse, HttpResponseNotFound
from django.http.response import JsonResponse
from userlist.models import User
from userlist.models import Info
from django.core.exceptions import ObjectDoesNotExist

def get_user_list_action(request):
    """
        ユーザリスト情報表示のアクション
            return JsonResponse({"userlist":user_list})
            存在するユーザリストをパラメータ指定された場合
            ユーザリストのメッセージがJsonで表示される
    """

    user_list = []

    for users in User.objects.all().values():
        try:
            user_list.append({"user_id":users['user_id'], "user_name":users['user_name']})
        except ObjectDoesNotExist:
            print '失敗しました'
    return JsonResponse({"userlist":user_list})
