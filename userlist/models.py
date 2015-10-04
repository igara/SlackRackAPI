# coding: UTF-8
from django.db import models

class User(models.Model):
    """
    ユーザモデル
    """
    user_id = models.CharField(max_length=200)
    user_name = models.CharField(max_length=200)

    def __unicode__(self):
        return self.user_name

class Info(models.Model):
    """
    ユーザ情報モデル
    """
    user = models.ForeignKey(User)

    def __unicode__(self):
        return self.user