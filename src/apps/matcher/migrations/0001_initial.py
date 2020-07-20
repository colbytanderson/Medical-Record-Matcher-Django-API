# Generated by Django 3.0.8 on 2020-07-20 02:31

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Record',
            fields=[
                ('title', models.CharField(max_length=200, primary_key=True, serialize=False)),
                ('confidenceScore', models.FloatField(default=0, validators=[django.core.validators.MaxValueValidator(1), django.core.validators.MinValueValidator(0)])),
                ('editors', models.ManyToManyField(related_name='record_editor', to=settings.AUTH_USER_MODEL)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='record_owner', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Column',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('confidenceScore', models.FloatField(default=0, validators=[django.core.validators.MaxValueValidator(1), django.core.validators.MinValueValidator(0)])),
                ('dataType', models.CharField(choices=[('name', 'name'), ('number', 'number'), ('state', 'state'), ('street', 'street'), ('dob', 'dob')], max_length=3)),
                ('record', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='matcher.Record')),
            ],
        ),
    ]