# Generated by Django 3.1.7 on 2021-04-08 08:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Branch',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('branchName', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': 'Branch',
                'verbose_name_plural': 'Branches',
            },
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('section', models.CharField(max_length=1)),
                ('courseName', models.CharField(max_length=50)),
                ('credits', models.IntegerField(default=0)),
                ('studentCap', models.IntegerField(default=0)),
                ('courseDescription', models.TextField()),
                ('program', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('departmentName', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': 'Department',
                'verbose_name_plural': 'Departments',
            },
        ),
        migrations.CreateModel(
            name='UserRole',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(max_length=50)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'UserRole',
                'verbose_name_plural': 'UserRoles',
            },
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rollNumber', models.IntegerField(unique=True)),
                ('graduationYear', models.IntegerField()),
                ('profilePicture', models.ImageField(upload_to='Profile Pictures/Students/')),
                ('batch', models.CharField(max_length=50)),
                ('program', models.CharField(max_length=50)),
                ('branch', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Core.branch')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Student',
                'verbose_name_plural': 'Students',
            },
        ),
        migrations.CreateModel(
            name='PreReq',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='preReqs', to='Core.course')),
                ('preReqCourse', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='preReqOf', to='Core.course')),
            ],
            options={
                'verbose_name': 'PreReq',
                'verbose_name_plural': 'PreReqs',
            },
        ),
        migrations.CreateModel(
            name='Faculty',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profilePicture', models.ImageField(upload_to='Profile Pictures/Faculties/')),
                ('profileLink', models.URLField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Faculty',
                'verbose_name_plural': 'Faculties',
            },
        ),
        migrations.CreateModel(
            name='DOAA',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profilePicture', models.ImageField(upload_to='Profile Pictures/DOAA/')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'DOAA',
                'verbose_name_plural': 'DOAA',
            },
        ),
        migrations.CreateModel(
            name='CourseFaculty',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='taughtBy', to='Core.course')),
                ('faculty', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='teaches', to='Core.faculty')),
            ],
            options={
                'verbose_name': 'CourseFaculty',
                'verbose_name_plural': 'CourseFaculties',
            },
        ),
        migrations.AddField(
            model_name='course',
            name='department',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Core.department'),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timeStamp', models.DateTimeField(auto_now=True)),
                ('content', models.CharField(max_length=500)),
                ('parentComment', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='parentOf', to='Core.comment')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='AntiReq',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('antiReqCourse', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='antiReqOf', to='Core.course')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='antiReqs', to='Core.course')),
            ],
            options={
                'verbose_name': 'AntiReq',
                'verbose_name_plural': 'AntiReqs',
            },
        ),
        migrations.CreateModel(
            name='Announcement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timeStamp', models.DateTimeField(auto_now=True)),
                ('content', models.CharField(max_length=500)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profilePicture', models.ImageField(upload_to='Profile Pictures/Admins/')),
                ('program', models.CharField(max_length=50)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Admin',
                'verbose_name_plural': 'Admins',
            },
        ),
    ]
