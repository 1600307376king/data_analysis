# Generated by Django 3.0.2 on 2020-01-23 03:32

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CpuInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=101, verbose_name='cpu型号')),
                ('physics_cores', models.IntegerField(default=0, verbose_name='cpu核心数')),
                ('logical_processors', models.IntegerField(default=0, verbose_name='线程数')),
                ('turbo', models.FloatField(default=0, verbose_name='cpu睿频')),
                ('utilization', models.FloatField(default=0, verbose_name='cpu占用率')),
                ('cur_frequency', models.FloatField(default=0, verbose_name='cpu当前频率')),
            ],
            options={
                'verbose_name': 'cpu',
                'verbose_name_plural': 'cpu',
            },
        ),
        migrations.CreateModel(
            name='MemoryInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='内存型号')),
                ('total_size', models.FloatField(default=0, verbose_name='内存大小')),
                ('max_frequency', models.FloatField(default=0, verbose_name='最高频率')),
                ('used', models.FloatField(default=0, verbose_name='内存已使用')),
            ],
        ),
        migrations.CreateModel(
            name='SolidStateDisk',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='固态硬盘型号')),
                ('total_size', models.FloatField(default=0, verbose_name='硬盘大小')),
                ('read_speed', models.FloatField(default=0, verbose_name='读取速度')),
                ('write_speed', models.FloatField(default=0, verbose_name='写入速度')),
                ('average_response_time', models.FloatField(default=0, verbose_name='平均响应时间')),
            ],
        ),
    ]
