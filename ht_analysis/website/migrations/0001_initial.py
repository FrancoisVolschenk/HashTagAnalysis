# Generated by Django 4.1.1 on 2022-11-09 07:35

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.TextField()),
                ('Age', models.IntegerField()),
                ('Active', models.BooleanField()),
            ],
        ),
    ]
