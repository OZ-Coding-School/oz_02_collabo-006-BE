# Generated by Django 5.0.6 on 2024-05-18 02:31

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("comments", "0005_rename_paraent_comment_comment_recomment"),
    ]

    operations = [
        migrations.RenameField(
            model_name="comment",
            old_name="recomment",
            new_name="parent_comment",
        ),
    ]