__author__ = 'Mikhail'
# -*- coding: utf-8 -*-

import vk_helpers

import urllib
import json

def get_last_post(group):
    url = 'http://api.vk.com/method/wall.get?domain={0}&count=3'.format(group)
    response = urllib.urlopen(url)
    text = json.loads(response.read())
    return "\n".join(text['response'][3]['text'].split("<br>"))

url = 'http://api.vk.com/method/board.getComments?group_id=55819158&topic_id=28747681'

# def get_daily_posts():
#
#
# def get_random_photo():
#
# def get_random_video():
#
#
def get_schedule():
    comments = vk_helpers.get_comments(u'РАСПИСАНИЕ И СТОИМОСТЬ ТРЕНИРОВОК!')
    return "\n".join(comments['response']['comments'][1]['text'].split("<br>"))


def get_schedule_photo():
    comments = vk_helpers.get_comments(u'РАСПИСАНИЕ И СТОИМОСТЬ ТРЕНИРОВОК!')
    photo_url = comments['response']['comments'][1]['attachments'][0]['photo']['src_big']
    photo_local = open('out.jpg', 'wb')
    photo_local.write(urllib.urlopen(photo_url).read())
    photo_local.close()
    return open('out.jpg', 'rb')


def get_repost_photo(photo_url):
    photo_url = photo_url
    photo_local = open('repost.jpg', 'wb')
    photo_local.write(urllib.urlopen(photo_url).read())
    photo_local.close()
    return open('repost.jpg', 'rb')

# def get_price():

