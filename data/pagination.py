#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2020/2/11 18:21
# @Author  : HelloWorld
# @File    : pagination.py
from rest_framework import pagination


class DataPagination(pagination.PageNumberPagination):
    page_query_param = "page"
    page_size = 2
    page_size_query_param = "size"
    max_page_size = None

