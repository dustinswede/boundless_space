# Generated by Django 3.2 on 2022-09-30 20:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='body',
            name='type',
            field=models.CharField(default='planet', max_length=50),
            preserve_default=False,
        ),
    ]
