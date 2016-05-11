# -*- coding: utf-8 -*-

import json
import logging
import requests
import urllib

import eventlet


def get_group_id(group_name):
    url = 'http://api.vk.com/method/groups.getById?group_id={}'.format(group_name)
    response = urllib.urlopen(url)
    group_info = json.loads(response.read())
    return group_info['response'][0]['gid']


def get_topic(topic_name):
    url = 'http://api.vk.com/method/board.getTopics?group_id={}'.format(get_group_id('roninfamily'))
    response = urllib.urlopen(url)
    topics = json.loads(response.read())
    for topic in topics['response']['topics'][1:]:
        if topic['title'] == topic_name:
            return topic['tid']


def get_comments(topic_name):
    url = 'http://api.vk.com/method/board.getComments?group_id={0}&topic_id={1}'.format(
        get_group_id('roninfamily'),
        get_topic(topic_name))
    response = urllib.urlopen(url)
    return json.loads(response.read())


def get_posts_from_wall():
    timeout = eventlet.Timeout(10)
    try:
        url = 'http://api.vk.com/method/wall.get?owner_id=336820&count=3'
        feed = requests.get(url)
        return feed.json()
    except eventlet.timeout.Timeout:
        logging.warning('Got Timeout while retrieving VK JSON data. Cancelling...')
        return None
    finally:
        timeout.cancel()

