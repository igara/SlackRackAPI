# coding: UTF-8
from django.conf.urls import patterns, include, url
from django.contrib import admin

from slackrack import views
import channelist.views
import privategrouplist.views
import userlist.views

admin.autodiscover()
urlpatterns = patterns('',
    # Examples:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^slack/channelist/', channelist.views.get_channel_list_action),
    url(r'^slack/channelistjson/', channelist.views.get_channel_list_json_action),
    url(r'^slack/privategrouplist/', privategrouplist.views.get_group_list_action),
    url(r'^slack/userlist/', userlist.views.get_user_list_action),
)
