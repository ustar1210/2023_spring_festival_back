# Generated by Django 4.2.1 on 2023-05-18 01:50

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("booth", "0004_alter_like_key_alter_menuimage_booth"),
    ]

    operations = [
        migrations.AlterField(
            model_name="like",
            name="key",
            field=models.CharField(
                blank=True, default="%+Wp0qof#8", editable=False, max_length=10
            ),
        ),
    ]
