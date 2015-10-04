# coding: UTF-8
from django.contrib import admin
from privategrouplist.models import Info, PrivateGroup

class InfoInline(admin.StackedInline):
  """
    プライベートグループ用の管理画面設定クラス
  """
  model = Info
  # Info入力項目数
  extra = 1

class PrivateGroupListAdmin(admin.ModelAdmin):
  """
    DBからプライベートグループを取得する
  """
  # 表示レイアウト
  fieldsets = [
    (None, { 'fields': ['group_id']}),
    (None, { 'fields': ['group_name']}),
  ]
  inlines = [InfoInline]
  # 表示項目
  list_display = ('group_id', 'group_name')
  

admin.site.register(PrivateGroup, PrivateGroupListAdmin)