# Generated by Django 3.2 on 2022-10-06 18:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_alter_project_body'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='body',
        ),
        migrations.CreateModel(
            name='ProjectAssignedBody',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('use_key', models.CharField(max_length=50)),
                ('body', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='project_assigned_bodies', to='core.body')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='project_assigned_bodies', to='core.project')),
            ],
        ),
    ]
