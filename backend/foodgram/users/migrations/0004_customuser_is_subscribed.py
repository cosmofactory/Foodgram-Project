# Generated by Django 4.2.1 on 2023-06-03 21:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_customuser_first_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='is_subscribed',
            field=models.BooleanField(blank=True, null=True),
        ),
    ]
