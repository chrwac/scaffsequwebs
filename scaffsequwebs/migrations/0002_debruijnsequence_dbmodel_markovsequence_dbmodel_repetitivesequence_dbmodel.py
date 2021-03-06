# Generated by Django 2.0.2 on 2018-03-14 19:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scaffsequwebs', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DeBruijnSequence_DBModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_name', models.CharField(default='', max_length=250)),
                ('sequ_name', models.CharField(default='', max_length=250)),
                ('db_order', models.IntegerField()),
                ('sequ_length', models.IntegerField()),
                ('sequence', models.CharField(max_length=30000)),
            ],
        ),
        migrations.CreateModel(
            name='MarkovSequence_DBModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_name', models.CharField(default='', max_length=250)),
                ('sequ_name', models.CharField(default='', max_length=250)),
                ('markov_order', models.IntegerField()),
                ('sequ_length', models.IntegerField()),
                ('sequence', models.CharField(max_length=30000)),
            ],
        ),
        migrations.CreateModel(
            name='RepetitiveSequence_DBModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_name', models.CharField(default='', max_length=250)),
                ('sequ_name', models.CharField(default='', max_length=250)),
                ('length_of_variable_part', models.IntegerField()),
                ('sequ_length', models.IntegerField()),
                ('sequence', models.CharField(max_length=30000)),
            ],
        ),
    ]
