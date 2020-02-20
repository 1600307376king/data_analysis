#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2020/2/11 10:54
# @Author  : HelloWorld
# @File    : permissions.py
from rest_framework import permissions


# class IsOwnerReadOnly(permissions.BasePermission):
#     def has_object_permission(self, request, view, obj):
#         if request.method in permissions.SAFE_METHODS:
#             return True
#
#         return obj.owner == request.user
