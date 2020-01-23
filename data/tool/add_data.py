#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2020/1/23 20:20
# @Author  : HelloWorld
# @File    : add_data.py
from data.models.common import CpuInfo, MemoryInfo, SolidStateDisk, NetInfo
import psutil
import platform


def add_latest_cpu_info():
    cpu_name = platform.processor()
    physics_cores = psutil.cpu_count(logical=False)
    logical_processors = psutil.cpu_count()
    turbo = psutil.cpu_freq().max
    cpu_utilization = psutil.cpu_percent()
    cur_frequency = psutil.cpu_freq().current
    CpuInfo.objects.create(name=cpu_name, physics_cores=physics_cores, logical_processors=logical_processors,
                           turbo=turbo, utilization=cpu_utilization, cur_frequency=cur_frequency)


def add_latest_memory_info():
    total_size = psutil.virtual_memory().total
    ava_size = psutil.virtual_memory().available
    used = psutil.virtual_memory().used
    memory_percent = psutil.virtual_memory().percent
    MemoryInfo.objects.create(total_size=total_size, ava_size=ava_size,
                              used=used, memory_percent=memory_percent)


def add_latest_disk_info():
    name = psutil.disk_partitions()[0].device
    total_size = psutil.virtual_memory().available
    read_speed = (psutil.disk_io_counters().read_bytes /
                  psutil.disk_io_counters().read_time) / 1024 ** 2
    write_speed = (psutil.disk_io_counters().write_bytes /
                   psutil.disk_io_counters().write_time) / 1024 ** 2
    SolidStateDisk.objects.create(name=name, total_size=total_size,
                                  read_speed=read_speed, write_speed=write_speed)


def add_latest_net_info():
    sent = int(psutil.net_io_counters().bytes_sent / 1024)
    recv = int(psutil.net_io_counters().bytes_recv / 1024)
    NetInfo.objects.create(bytes_sent=sent, bytes_recv=recv)
