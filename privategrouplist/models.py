# coding: UTF-8
from django.db import models

class PrivateGroup(models.Model):
    """
    プライベートグループモデル
    """
    group_id = models.CharField(max_length=200)
    group_name = models.CharField(max_length=200)

    def __unicode__(self):
        return self.group_name

class Info(models.Model):
    """
    プライベートグループ情報モデル
    """
    group = models.ForeignKey(PrivateGroup)
    message_text = models.CharField(max_length=200)
    message_user = models.CharField(max_length=200)
    message_time_stamp = models.CharField(max_length=200)

    def __unicode__(self):
        return self.message_text