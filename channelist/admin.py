# coding: UTF-8
from django.contrib import admin
from channelist.models import Info, Channel

class InfoInline(admin.StackedInline):
  """
    チャンネルリスト用の管理画面設定クラス
  """

  model = Info
  # Info入力項目数
  extra = 1

class ChannelistAdmin(admin.ModelAdmin):
  """
    DBからチャンネルリストを取得する
  """

  # 表示レイアウト
  fieldsets = [
    (None, { 'fields': ['channel_id']}),
    (None, { 'fields': ['channel_name']}),
  ]
  inlines = [InfoInline]
  # 表示項目
  list_display = ('channel_id', 'channel_name')
  

admin.site.register(Channel, ChannelistAdmin)