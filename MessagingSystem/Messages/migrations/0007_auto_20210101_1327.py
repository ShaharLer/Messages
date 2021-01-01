# Generated by Django 3.1.4 on 2021-01-01 11:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Messages', '0006_auto_20210101_1321'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='sender',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='sender', to='Messages.systemuser'),
        ),
    ]