# Generated by Django 2.1.5 on 2019-07-21 16:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classes', '0003_auto_20190721_1842'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='exam_grade',
            field=models.CharField(choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'), ('F', 'F')], max_length=1),
        ),
    ]