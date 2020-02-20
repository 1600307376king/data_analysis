#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2020/2/8 18:58
# @Author  : HelloWorld
# @File    : serializers.py
from rest_framework import serializers
from data.models.common import CpuInfo, MemoryInfo, SolidStateDisk, NetInfo, MyUser
import psutil
import datetime


class CpuSerializer(serializers.ModelSerializer):
    class Meta:
        model = CpuInfo
        fields = ('utilization', 'update_time')

    def to_representation(self, instance):
        data = super(CpuSerializer, self).to_representation(instance)
        data['utilization'] = psutil.cpu_percent()
        data['update_time'] = datetime.datetime.now().strftime('%H:%M:%S')
        return data


class MemorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MemoryInfo
        fields = ('memory_percent',)

    def create(self, validated_data):
        pass

    # 自定义数据库数据
    def to_representation(self, instance):
        data = super(MemorySerializer, self).to_representation(instance)
        data['memory_percent'] = psutil.virtual_memory().percent
        return data


class SolidStateDiskSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        data = super(SolidStateDiskSerializer, self).to_representation(instance)
        data['read_speed'] = (psutil.disk_io_counters().read_bytes /
                              psutil.disk_io_counters().read_time) / 1024 ** 2

        data['write_speed'] = (psutil.disk_io_counters().write_bytes /
                               psutil.disk_io_counters().write_time) / 1024 ** 2

        return data

    class Meta:
        model = SolidStateDisk
        fields = '__all__'


class NetSerializer(serializers.ModelSerializer):
    class Meta:
        model = NetInfo
        fields = '__all__'

    def to_representation(self, instance):
        data = super(NetSerializer, self).to_representation(instance)
        data['bytes_sent'] = int(psutil.net_io_counters().bytes_sent / 1024)

        data['bytes_recv'] = int(psutil.net_io_counters().bytes_recv / 1024)

        return data


class MyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = '__all__'
