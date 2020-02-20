from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from data.tool.add_data import *
from django.utils.translation import gettext
import platform
import psutil
import datetime
import json
from data import tasks
from django.views.generic.base import View
from data.serializers import CpuSerializer, MemorySerializer, SolidStateDiskSerializer, NetSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from rest_framework import viewsets, status, mixins
from rest_framework.decorators import api_view
from django.http import Http404
from data.models.common import MyUser
from data.serializers import MyUserSerializer
from drf_multiple_model.views import ObjectMultipleModelAPIView
from data import pagination
from rest_framework.metadata import SimpleMetadata


# Create your views here.


def home(request):
    context = {

    }
    return render(request, 'home.html', context)


def index(request, *args, **kwargs):
    res = tasks.send_email.delay('1600307376@qq.com', 'qwe321')
    return JsonResponse({'status': 'successful', 'task_id': res.task_id})


def test(request):
    context = {
        'category': gettext('hi, boys'),
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


class CpuMessageSet(viewsets.ModelViewSet):
    queryset = CpuInfo.objects.all()
    serializer_class = CpuSerializer


# 自定义响应内容
@api_view(['GET', 'POST'])
def memory_list(request):
    if request.method == 'GET':
        memory_msg = MemoryInfo.objects.all()
        response = {
            'code': 0,
            'data': {
                'utilization': psutil.cpu_percent(),

                'memory_percent': psutil.virtual_memory().percent,
                'read_speed': (psutil.disk_io_counters().read_bytes /
                               psutil.disk_io_counters().read_time) / 1024 ** 2,
                'write_speed': (psutil.disk_io_counters().write_bytes /
                                psutil.disk_io_counters().write_time) / 1024 ** 2,
                'bytes_sent': int(psutil.net_io_counters().bytes_sent / 1024),
                'bytes_recv': int(psutil.net_io_counters().bytes_recv / 1024),
                'update_time': datetime.datetime.now().strftime('%H:%M:%S'),

            },
            'msg': 'success',
            'total': ''
        }

        serializer = MemorySerializer(memory_msg, many=True)
        # response['data'] = serializer.data
        # response['total'] = len(serializer.data)
        return Response(response, template_name='home.html')
    elif request.method == 'POST':
        serializer = MemorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def memory_control(request, pk):
    try:
        memory_obj = MemoryInfo.objects.get(id=pk)
    except MemoryInfo.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = MemorySerializer(memory_obj)
        return Response(serializer.data)

    elif request.method == 'PUT':

        serializer = MemorySerializer(memory_obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        memory_obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# 对磁盘数据分页
class SolidStateDiskList(APIView):
    @staticmethod
    def get(request, format=None):
        ssd = SolidStateDisk.objects.all()

        page_obj = pagination.DataPagination()
        page_data = page_obj.paginate_queryset(ssd, request)
        serializer = SolidStateDiskSerializer(page_data, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = SolidStateDiskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SolidStateControl(APIView):
    def get_object(self, pk):
        try:
            return SolidStateDisk.objects.get(pk=pk)
        except SolidStateDisk.DoesNotExist:
            return Http404

    def get(self, request, pk, format=None):
        ssd = self.get_object(pk)
        serializer = SolidStateDiskSerializer(ssd)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        ssd = self.get_object(pk)
        serializer = SolidStateDiskSerializer(ssd, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        ssd = self.get_object(pk)
        ssd.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class NetList(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    queryset = NetInfo.objects.all()
    serializer_class = NetSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class NetControl(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    queryset = NetInfo.objects.all()
    serializer_class = NetSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class NetToList(generics.ListCreateAPIView):
    queryset = NetInfo.objects.all()
    serializer_class = NetSerializer


class NetToControl(generics.RetrieveUpdateAPIView):
    queryset = NetInfo.objects.all()
    serializer_class = NetSerializer


class MyUserList(generics.ListCreateAPIView):
    queryset = MyUser.objects.all()
    serializer_class = MyUserSerializer


class MyUserControl(generics.RetrieveUpdateDestroyAPIView):
    queryset = MyUser.objects.all()
    serializer_class = MyUserSerializer


class SystemInfoList(ObjectMultipleModelAPIView):
    asd = CpuInfo.objects.all()
    querylist = [
        {'queryset': CpuInfo.objects.all(), 'serializer_class': CpuSerializer},
        {'queryset': MemoryInfo.objects.all(), 'serializer_class': MemorySerializer},
        {'queryset': SolidStateDisk.objects.all(), 'serializer_class': SolidStateDiskSerializer},
        {'queryset': NetInfo.objects.all(), 'serializer_class': NetSerializer},
    ]

# class ModelNamePagination(PageNumberPagination):
#     page_size = 10
#     page_size_query_param = 'page_size'
#     max_page_size = 100
#     page_query_param = 'p'
#
#
# class ModuleNameList(generics.ListCreateAPIView):
#     pagination_class = ModelNamePagination
