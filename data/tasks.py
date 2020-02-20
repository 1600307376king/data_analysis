#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2020/2/6 14:37
# @Author  : HelloWorld
# @File    : tasks.py
from __future__ import absolute_import, unicode_literals
from celery import shared_task
from django.core.mail import send_mail


@shared_task
def add(x, y):
    return x + y


@shared_task
def mul(x, y):
    return x * y


@shared_task
def send_email(recipient, code):
    res = send_mail('注册通知', '验证码：{}'.format(code), '1600307376@qq.com', [recipient])
    return res
