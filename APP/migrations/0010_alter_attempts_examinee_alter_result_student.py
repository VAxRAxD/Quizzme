# Generated by Django 4.1 on 2022-11-01 08:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('APP', '0009_alter_attempts_examinee_alter_result_student'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attempts',
            name='examinee',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='result',
            name='student',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
