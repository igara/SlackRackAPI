# coding: UTF-8
from django.db import models

class Im(models.Model):
    """
    ダイレクトメッセージモデル
    """
    im_id = models.CharField(max_length=200)
    im_name = models.CharField(max_length=200)

    def __unicode__(self):
        return self.im_name

class Info(models.Model):
    """
    ダイレクトメッセージ情報モデル
    """
    im = models.ForeignKey(Im)
    message_text = models.CharField(max_length=200)
    message_user = models.CharField(max_length=200)
    message_time_stamp = models.CharField(max_length=200)

    def __unicode__(self):
        return self.message_text