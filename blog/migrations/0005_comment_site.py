# Generated by Django 2.2.7 on 2020-01-04 17:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_auto_20200104_1935'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='site',
            field=models.CharField(default=1, max_length=50, verbose_name='الموقع :'),
            preserve_default=False,
        ),
    ]