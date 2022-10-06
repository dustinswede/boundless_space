# Generated by Django 3.2 on 2022-10-05 19:01

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_auto_20221005_1824'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='body',
            options={'verbose_name_plural': 'bodies'},
        ),
        migrations.AlterModelOptions(
            name='colony',
            options={'verbose_name_plural': 'colonies'},
        ),
        migrations.CreateModel(
            name='Building',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('type', models.CharField(max_length=50)),
                ('colony', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='buildings', to='core.colony')),
            ],
        ),
    ]
