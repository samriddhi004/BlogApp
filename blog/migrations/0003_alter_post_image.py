# Generated by Django 5.1.1 on 2024-10-15 06:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0002_post_image_alter_post_slug"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="image",
            field=models.ImageField(upload_to="posts"),
        ),
    ]