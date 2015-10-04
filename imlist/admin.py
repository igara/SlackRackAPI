# coding: UTF-8
from django.contrib import admin
from imlist.models import Info, Im

class InfoInline(admin.StackedInline):
  """
    ダイレクトメッセージ用の管理画面設定クラス
  """
  model = Info
  # Info入力項目数
  extra = 1

class ImListAdmin(admin.ModelAdmin):
  """
    DBからダイレクトメッセージを取得する
  """
  # 表示レイアウト
  fieldsets = [
    (None, { 'fields': ['im_id']}),
    (None, { 'fields': ['im_name']}),
  ]
  inlines = [InfoInline]
  # 表示項目
  list_display = ('im_id', 'im_name')
  

admin.site.register(Im, ImListAdmin)