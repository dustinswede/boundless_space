# Generated by Django 3.2 on 2022-10-06 17:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_auto_20221005_1901'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='fleet',
        ),
        migrations.CreateModel(
            name='ProjectFleet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('use_key', models.CharField(max_length=50)),
                ('fleet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='project_fleets', to='core.fleet')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='project_fleets', to='core.project')),
            ],
        ),
    ]
