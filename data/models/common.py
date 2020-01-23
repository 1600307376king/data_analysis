from django.db import models
from django.utils import timezone
import datetime

# Create your models here.
# cur_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


class CpuInfo(models.Model):
    name = models.CharField('cpu型号', max_length=101)
    physics_cores = models.IntegerField(default=0, verbose_name='cpu核心数')
    logical_processors = models.IntegerField(default=0, verbose_name='线程数')
    turbo = models.FloatField(default=0, verbose_name='cpu睿频')
    utilization = models.FloatField(default=0, verbose_name='cpu占用率')
    cur_frequency = models.FloatField(default=0, verbose_name='cpu当前频率')
    update_time = models.DateTimeField('更新时间', default=timezone.now())

    class Meta:
        verbose_name = 'cpu'
        verbose_name_plural = 'cpu'

    def __str__(self):
        return self.name


class MemoryInfo(models.Model):
    total_size = models.FloatField(default=0, verbose_name='内存大小')
    ava_size = models.FloatField(default=0, verbose_name='内存可用大小')
    used = models.FloatField(default=0, verbose_name='内存已使用大小')
    memory_percent = models.FloatField(default=0, verbose_name='内存使用百分比')
    update_time = models.DateTimeField('更新时间', auto_now=True)

    # def __str__(self):
    #     return self.name


class SolidStateDisk(models.Model):
    name = models.CharField('固态硬盘型号', max_length=100)
    total_size = models.FloatField(default=0, verbose_name='硬盘大小')
    read_speed = models.FloatField(default=0, verbose_name='读取速度')
    write_speed = models.FloatField(default=0, verbose_name='写入速度')
    update_time = models.DateTimeField('更新时间', auto_now=True)

    def __str__(self):
        return self.name


class NetInfo(models.Model):
    bytes_sent = models.FloatField(default=0, verbose_name='发送')
    bytes_recv = models.FloatField(default=0, verbose_name='接受')
    update_time = models.DateTimeField('更新时间', auto_now=True)



