# Generated by Django 5.0.6 on 2024-05-08 08:17

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("hashtags", "0003_alter_hashtag_table"),
    ]

    operations = [
        migrations.RenameField(
            model_name="hashtag",
            old_name="hashtag",
            new_name="content",
        ),
    ]