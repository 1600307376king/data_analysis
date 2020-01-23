from django.shortcuts import render
from django.http import HttpResponse
from data.models.common import CpuInfo, MemoryInfo, SolidStateDisk, NetInfo
from data.tool.add_data import *
import platform
import psutil
import datetime
import json


# Create your views here.


def home(request):
    context = {

    }
    return render(request, 'home.html', context)


def test(request):
    context = {
        'category': 'a',
    }
    return render(request, 'test.html', context)


# 单次获取数据库系统数据
def get_first_system_info(request):
    latest_num = 4
    cpu_obj = CpuInfo.objects.order_by('update_time')[:latest_num]
    memory_obj = MemoryInfo.objects.order_by('update_time')[:latest_num]
    disk_obj = SolidStateDisk.objects.order_by('update_time')[:latest_num]
    network_obj = NetInfo.objects.order_by('update_time')[:latest_num]
    res = {
        'cpu': [i.utilization for i in cpu_obj],
        'memory': [i.memory_percent for i in memory_obj],
        'disk_r': [i.read_speed for i in disk_obj],
        'disk_w': [i.write_speed for i in disk_obj],
        'net_s': [i.bytes_sent for i in network_obj],
        'net_r': [i.bytes_recv for i in network_obj],
        'cur_t': [(datetime.datetime.now() - datetime.timedelta(seconds=i)).strftime('%H:%M:%S')
                  for i in range(latest_num).__reversed__()],
    }

    return HttpResponse(json.dumps(res), content_type='application/json')


# 前端定时请求获取数据
def get_system_info(request):
    cpu_utilization = psutil.cpu_percent()
    memory_used_rate = psutil.virtual_memory().used / psutil.virtual_memory().total * 100
    disk_read_speed = (psutil.disk_io_counters().read_bytes /
                       psutil.disk_io_counters().read_time) / 1024 ** 2
    disk_write_speed = (psutil.disk_io_counters().write_bytes /
                        psutil.disk_io_counters().write_time) / 1024 ** 2
    bytes_sent = int(psutil.net_io_counters().bytes_sent / 1024)
    bytes_recv = int(psutil.net_io_counters().bytes_recv / 1024)
    cur_time = datetime.datetime.now().strftime('%H:%M:%S')

    res = {
        'cpu': cpu_utilization,
        'memory': memory_used_rate,
        'disk_r': disk_read_speed,
        'disk_w': disk_write_speed,
        'net_s': bytes_sent,
        'net_r': bytes_recv,
        'cur_t': cur_time
    }

    return HttpResponse(json.dumps(res), content_type='application/json')


def add_latest_info(request):
    try:
        add_latest_cpu_info()
        add_latest_disk_info()
        add_latest_memory_info()
        add_latest_net_info()
        return HttpResponse('add_ok')
    except Exception as e:
        print(e)
        return HttpResponse('add_error')
