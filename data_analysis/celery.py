#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2020/2/6 14:34
# @Author  : HelloWorld
# @File    : celery.py
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'data_analysis.settings')  # 设置django环境

app = Celery('data_analysis')

app.config_from_object('django.conf:settings', namespace='CELERY')  # 使用CELERY_ 作为前缀，在settings中写配置

app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))