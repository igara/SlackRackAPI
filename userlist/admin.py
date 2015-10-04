# coding: UTF-8
from django.contrib import admin
from userlist.models import Info, User

class InfoInline(admin.StackedInline):
  """
    ユーザリスト用の管理画面設定クラス
  """
  model = Info
  # Info入力項目数
  extra = 1

class UserListAdmin(admin.ModelAdmin):
  """
    DBからユーザリストを取得する
  """
  # 表示レイアウト
  fieldsets = [
    (None, { 'fields': ['user_id']}),
    (None, { 'fields': ['user_name']}),
  ]
  inlines = [InfoInline]
  # 表示項目
  list_display = ('user_id', 'user_name')
  

admin.site.register(User, UserListAdmin)