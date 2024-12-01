# Generated by Django 5.1.2 on 2024-10-24 22:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0009_remove_sorgulamasonucu_daire_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sorgulamasonucu',
            name='abonent_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='sorgulamasonucu',
            name='aile_terkibi',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='sorgulamasonucu',
            name='emlak_sonuc',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='sorgulamasonucu',
            name='infocenter_sonuc',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='sorgulamasonucu',
            name='phone_number',
            field=models.CharField(max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='sorgulamasonucu',
            name='tax_sonuc',
            field=models.JSONField(blank=True, null=True),
        ),
    ]
