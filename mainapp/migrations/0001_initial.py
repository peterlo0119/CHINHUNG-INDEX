# Generated by Django 5.2.3 on 2025-06-23 13:56

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AogiriChannel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('channel_url', models.URLField()),
                ('channel_avatar', models.URLField(blank=True, null=True)),
                ('group_name', models.CharField(blank=True, max_length=50, null=True)),
                ('latest_video_title', models.CharField(blank=True, max_length=200, null=True)),
                ('latest_video_url', models.URLField(blank=True, null=True)),
                ('latest_video_thumbnail', models.URLField(blank=True, null=True)),
                ('latest_video_duration', models.CharField(blank=True, max_length=20, null=True)),
                ('latest_video_views', models.CharField(blank=True, max_length=20, null=True)),
                ('latest_video_published', models.CharField(blank=True, max_length=50, null=True)),
                ('live_title', models.CharField(blank=True, max_length=200, null=True)),
                ('live_url', models.URLField(blank=True, null=True)),
                ('live_thumbnail', models.URLField(blank=True, null=True)),
                ('live_start_time', models.CharField(blank=True, max_length=50, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='HololiveChannel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('channel_url', models.URLField()),
                ('channel_avatar', models.URLField(blank=True, null=True)),
                ('group_name', models.CharField(blank=True, max_length=50, null=True)),
                ('latest_video_title', models.CharField(blank=True, max_length=200, null=True)),
                ('latest_video_url', models.URLField(blank=True, null=True)),
                ('latest_video_thumbnail', models.URLField(blank=True, null=True)),
                ('latest_video_duration', models.CharField(blank=True, max_length=20, null=True)),
                ('latest_video_views', models.CharField(blank=True, max_length=20, null=True)),
                ('latest_video_published', models.CharField(blank=True, max_length=50, null=True)),
                ('live_title', models.CharField(blank=True, max_length=200, null=True)),
                ('live_url', models.URLField(blank=True, null=True)),
                ('live_thumbnail', models.URLField(blank=True, null=True)),
                ('live_start_time', models.CharField(blank=True, max_length=50, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='MilprChannel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('channel_url', models.URLField()),
                ('channel_avatar', models.URLField(blank=True, null=True)),
                ('group_name', models.CharField(blank=True, max_length=50, null=True)),
                ('latest_video_title', models.CharField(blank=True, max_length=200, null=True)),
                ('latest_video_url', models.URLField(blank=True, null=True)),
                ('latest_video_thumbnail', models.URLField(blank=True, null=True)),
                ('latest_video_duration', models.CharField(blank=True, max_length=20, null=True)),
                ('latest_video_views', models.CharField(blank=True, max_length=20, null=True)),
                ('latest_video_published', models.CharField(blank=True, max_length=50, null=True)),
                ('live_title', models.CharField(blank=True, max_length=200, null=True)),
                ('live_url', models.URLField(blank=True, null=True)),
                ('live_thumbnail', models.URLField(blank=True, null=True)),
                ('live_start_time', models.CharField(blank=True, max_length=50, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='NijisanjiChannel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('channel_url', models.URLField()),
                ('channel_avatar', models.URLField(blank=True, null=True)),
                ('group_name', models.CharField(blank=True, max_length=50, null=True)),
                ('latest_video_title', models.CharField(blank=True, max_length=200, null=True)),
                ('latest_video_url', models.URLField(blank=True, null=True)),
                ('latest_video_thumbnail', models.URLField(blank=True, null=True)),
                ('latest_video_duration', models.CharField(blank=True, max_length=20, null=True)),
                ('latest_video_views', models.CharField(blank=True, max_length=20, null=True)),
                ('latest_video_published', models.CharField(blank=True, max_length=50, null=True)),
                ('live_title', models.CharField(blank=True, max_length=200, null=True)),
                ('live_url', models.URLField(blank=True, null=True)),
                ('live_thumbnail', models.URLField(blank=True, null=True)),
                ('live_start_time', models.CharField(blank=True, max_length=50, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SelfChannel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('channel_url', models.URLField()),
                ('channel_avatar', models.URLField(blank=True, null=True)),
                ('group_name', models.CharField(blank=True, max_length=50, null=True)),
                ('latest_video_title', models.CharField(blank=True, max_length=200, null=True)),
                ('latest_video_url', models.URLField(blank=True, null=True)),
                ('latest_video_thumbnail', models.URLField(blank=True, null=True)),
                ('latest_video_duration', models.CharField(blank=True, max_length=20, null=True)),
                ('latest_video_views', models.CharField(blank=True, max_length=20, null=True)),
                ('latest_video_published', models.CharField(blank=True, max_length=50, null=True)),
                ('live_title', models.CharField(blank=True, max_length=200, null=True)),
                ('live_url', models.URLField(blank=True, null=True)),
                ('live_thumbnail', models.URLField(blank=True, null=True)),
                ('live_start_time', models.CharField(blank=True, max_length=50, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='VsingerChannel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('channel_url', models.URLField()),
                ('channel_avatar', models.URLField(blank=True, null=True)),
                ('group_name', models.CharField(blank=True, max_length=50, null=True)),
                ('latest_video_title', models.CharField(blank=True, max_length=200, null=True)),
                ('latest_video_url', models.URLField(blank=True, null=True)),
                ('latest_video_thumbnail', models.URLField(blank=True, null=True)),
                ('latest_video_duration', models.CharField(blank=True, max_length=20, null=True)),
                ('latest_video_views', models.CharField(blank=True, max_length=20, null=True)),
                ('latest_video_published', models.CharField(blank=True, max_length=50, null=True)),
                ('live_title', models.CharField(blank=True, max_length=200, null=True)),
                ('live_url', models.URLField(blank=True, null=True)),
                ('live_thumbnail', models.URLField(blank=True, null=True)),
                ('live_start_time', models.CharField(blank=True, max_length=50, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
