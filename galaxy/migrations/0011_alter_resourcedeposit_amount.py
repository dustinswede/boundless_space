# Generated by Django 3.2 on 2021-04-30 18:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('galaxy', '0010_alter_resourcestockpile_holding'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resourcedeposit',
            name='amount',
            field=models.PositiveBigIntegerField(),
        ),
    ]
