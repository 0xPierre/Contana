# Generated by Django 4.2.1 on 2023-05-25 16:13

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("user", "0003_alter_user_email"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="avatar",
            field=models.ImageField(blank=True, null=True, upload_to="avatars"),
        ),
    ]
