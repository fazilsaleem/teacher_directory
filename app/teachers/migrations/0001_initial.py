# Generated by Django 3.1.5 on 2021-01-27 05:24

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Subjects',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('subject_name', models.CharField(max_length=200)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Teachers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('email', models.CharField(max_length=100, unique=True)),
                ('phone_number', models.CharField(blank=True, max_length=20, null=True)),
                ('room_number', models.CharField(blank=True, max_length=20, null=True)),
                ('profile_picture', models.ImageField(blank=True, null=True, upload_to='teacher_profile')),
                ('organisation', models.CharField(blank=True, max_length=100, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('subjects_taught', models.ManyToManyField(blank=True, related_name='subjects', to='teachers.Subjects')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
