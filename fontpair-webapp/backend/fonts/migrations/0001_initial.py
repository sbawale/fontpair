# Generated by Django 2.2.7 on 2019-11-30 12:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Font',
            fields=[
                ('name', models.CharField(default=None, max_length=255, primary_key=True, serialize=False)),
                ('family', models.CharField(default=None, max_length=255)),
                ('category', models.CharField(default=None, max_length=255)),
                ('is_body', models.BooleanField(default=True)),
                ('is_serif', models.BooleanField(default=True)),
                ('is_italic', models.BooleanField(default=False)),
                ('weight', models.CharField(choices=[('thin', 'Thin'), ('extralight', 'Extra Light'), ('light', 'Light'), ('regular', 'Regular'), ('medium', 'Medium'), ('semibold', 'Semi Bold'), ('bold', 'Bold'), ('extrabold', 'Extra Bold'), ('black', 'Black')], default='regular', max_length=20)),
                ('url', models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name='Weight',
            fields=[
                ('weight', models.IntegerField(default=None, primary_key=True, serialize=False)),
                ('string', models.CharField(default=None, max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='FontPair',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('font1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='font1', to='fonts.Font')),
                ('font2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='font2', to='fonts.Font')),
            ],
            options={
                'verbose_name_plural': 'Pairings',
            },
        ),
    ]