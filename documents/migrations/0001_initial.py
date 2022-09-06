# Generated by Django 4.0.6 on 2022-08-07 13:08

from django.db import migrations, models
import django.db.models.deletion
import documents.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('grades', '0001_initial'),
        ('communications', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='section',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('section_name', models.CharField(max_length=20)),
                ('time_stamp', models.DateField(auto_now_add=True)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='grades.course')),
            ],
        ),
        migrations.CreateModel(
            name='replydocs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_name', models.CharField(default='', max_length=20)),
                ('document', models.FileField(upload_to=documents.models.reply_path)),
                ('reply', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='communications.reply')),
            ],
        ),
        migrations.CreateModel(
            name='folder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('folder_name', models.CharField(max_length=20)),
                ('desc', models.TextField(default='')),
                ('time_stamp', models.DateField(auto_now_add=True)),
                ('section', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='documents.section')),
            ],
        ),
        migrations.CreateModel(
            name='docs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_name', models.CharField(default='', max_length=20)),
                ('document', models.FileField(upload_to=documents.models.directory_path)),
                ('desc', models.TextField(default='')),
                ('time_stamp', models.DateField(auto_now_add=True)),
                ('folder', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='documents.folder')),
                ('section', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='documents.section')),
            ],
        ),
    ]
