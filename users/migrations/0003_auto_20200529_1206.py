# Generated by Django 2.2.8 on 2020-05-29 12:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_user_preferences'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='preferences',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, to='preferences.Preferences'),
            preserve_default=False,
        ),
    ]
