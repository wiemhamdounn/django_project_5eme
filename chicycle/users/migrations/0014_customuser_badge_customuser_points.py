# Generated by Django 5.1.1 on 2024-10-28 10:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0013_remove_userbadge_badge_remove_blogpost_category_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='badge',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='points',
            field=models.IntegerField(default=0),
        ),
    ]
