# Generated by Django 4.1.4 on 2022-12-27 18:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='variation',
            name='price',
            field=models.IntegerField(default=0),
        ),
    ]
