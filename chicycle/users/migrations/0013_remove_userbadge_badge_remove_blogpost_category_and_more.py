# Generated by Django 5.1.1 on 2024-10-28 10:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0012_alter_blogpost_category'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userbadge',
            name='badge',
        ),
        migrations.RemoveField(
            model_name='blogpost',
            name='category',
        ),
        migrations.RemoveField(
            model_name='userbadge',
            name='user',
        ),
        migrations.DeleteModel(
            name='Badge',
        ),
        migrations.DeleteModel(
            name='Category',
        ),
        migrations.DeleteModel(
            name='UserBadge',
        ),
    ]
