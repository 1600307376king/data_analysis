from django.shortcuts import render
from django.http import HttpResponse
from data.models.common import CpuInfo
import platform
import psutil
import datetime
import json


# Create your views here.


def home(request):
    cpu_obj = CpuInfo.objects.all()
    # print(cpu_obj[0].update_time)
    # print(type(cpu_obj[0].update_time))
    # print(cpu_obj[0].name)
    # cur_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    context = {
        'cpu': {'cpu_utilization': psutil.cpu_percent()},
        'memory': '666',
        'disk': '777',
    }
    print(datetime.datetime.now().strftime('%H:%M:%S'))
    print(cpu_obj[0].update_time.strftime('%H:%M:%S'))
    # system_info = dict()
    # system_info['cpu'] = {
    #     'cpu_utilization': psutil.cpu_percent(),
    # }
    # system_info['memory'] = '666'
    # system_info['disk'] = ''
    # print(system_info['cpu'])
    return render(request, 'home.html', context)


def test(request):
    context = {
        'category': 'a',
    }
    return render(request, 'test.html', context)


def get_system_info(request):
    cpu_utilization = psutil.cpu_percent()
    memory_used_rate = psutil.virtual_memory().used / psutil.virtual_memory().total * 100
    disk_read_speed = (psutil.disk_io_counters().read_bytes /
                       psutil.disk_io_counters().read_time) / 1024 ** 2
    disk_write_speed = (psutil.disk_io_counters().write_bytes /
                        psutil.disk_io_counters().write_time) / 1024 ** 2
    cur_time = datetime.datetime.now().strftime('%H:%M:%S')

    res = {
        'cpu': cpu_utilization,
        'memory': memory_used_rate,
        'disk_read': disk_read_speed,
        'disk_write': disk_write_speed,
        'cur_time': cur_time
    }

    return HttpResponse(json.dumps(res), content_type='application/json')


def add_latest_cpu_info(request):
    cpu_info = platform.processor()
    physics_cores = psutil.cpu_count(logical=False)
    logical_processors = psutil.cpu_count()
    turbo = psutil.cpu_freq().max
    cpu_utilization = psutil.cpu_percent()
    cur_frequency = psutil.cpu_freq().current
    CpuInfo.objects.create(name=cpu_info, physics_cores=physics_cores, logical_processors=logical_processors,
                           turbo=turbo, utilization=cpu_utilization, cur_frequency=cur_frequency)
    return HttpResponse('add_ok')
