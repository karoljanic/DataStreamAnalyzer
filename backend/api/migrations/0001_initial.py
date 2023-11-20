# Generated by Django 4.2.6 on 2023-11-20 23:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DataStream',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Type',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('stream', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.datastream')),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('stream', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.datastream')),
            ],
        ),
        migrations.CreateModel(
            name='DataSketch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.DateField()),
                ('sketch', models.BinaryField()),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.tag')),
                ('typ', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.type')),
            ],
        ),
        migrations.AddConstraint(
            model_name='datasketch',
            constraint=models.UniqueConstraint(fields=('day', 'tag', 'typ'), name='unique_keys'),
        ),
    ]
