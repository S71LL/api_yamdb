# Generated by Django 3.2 on 2023-03-27 20:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_user_token'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='token',
            field=models.CharField(blank=True, default='empty', max_length=254, verbose_name='Token'),
        ),
    ]
