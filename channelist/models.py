# coding: UTF-8
from django.db import models

class Channel(models.Model):
  """
  チャンネルモデル
  """

  channel_id = models.CharField(max_length=1000)
  channel_name = models.CharField(max_length=100)

  def __unicode__(self):
    return self.channel_name

class Info(models.Model):
  """
  チャンネル情報モデル
  """
  channel = models.ForeignKey(Channel)
  message_user = models.CharField(max_length=100)
  message_text = models.CharField(max_length=500, blank=True, null=True)
  attachments_fallback = models.CharField(max_length=500, blank=True, null=True)
  attachments_text = models.CharField(max_length=500, blank=True, null=True)
  message_time_stamp = models.CharField(max_length=200)

  def __unicode__(self):
    return self.message_text
