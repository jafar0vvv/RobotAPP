# Generated by Django 5.1.2 on 2024-10-24 05:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0007_sorgulamasonucu_mentqe_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='sorgulamasonucu',
            name='daire_id',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
