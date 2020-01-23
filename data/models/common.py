from django.db import models
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
    update_time = models.DateTimeField('更新时间', default=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    class Meta:
        verbose_name = 'cpu'
        verbose_name_plural = 'cpu'

    def __str__(self):
        return self.name


class MemoryInfo(models.Model):
    name = models.CharField('内存型号', max_length=100)
    total_size = models.FloatField(default=0, verbose_name='内存大小')
    max_frequency = models.FloatField(default=0, verbose_name='最高频率')
    used = models.FloatField(default=0, verbose_name='内存已使用')
    update_time = models.DateTimeField('更新时间', auto_now=True)

    def __str__(self):
        return self.name


class SolidStateDisk(models.Model):
    name = models.CharField('固态硬盘型号', max_length=100)
    total_size = models.FloatField(default=0, verbose_name='硬盘大小')
    read_speed = models.FloatField(default=0, verbose_name='读取速度')
    write_speed = models.FloatField(default=0, verbose_name='写入速度')
    average_response_time = models.FloatField(default=0, verbose_name='平均响应时间')
    update_time = models.DateTimeField('更新时间', auto_now=True)

    def __str__(self):
        return self.name


