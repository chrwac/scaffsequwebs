# Generated by Django 2.0.2 on 2018-03-10 20:47

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GeneratedSequence',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_name', models.CharField(max_length=250)),
                ('sequence', models.CharField(max_length=20000)),
                ('sequence_type', models.CharField(max_length=30)),
            ],
        ),
    ]