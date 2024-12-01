# Generated by Django 5.1.2 on 2024-11-07 11:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0012_sorgulamasonuclari_delete_sorgulamasonucu'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sorgulamasonuclari',
            name='ad',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='sorgulamasonuclari',
            name='cinsiyet',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='sorgulamasonuclari',
            name='dogum_tarixi',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='sorgulamasonuclari',
            name='fin_kod',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='sorgulamasonuclari',
            name='kimlik_numarasi',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='sorgulamasonuclari',
            name='kimlik_seri',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='sorgulamasonuclari',
            name='phone_number',
            field=models.CharField(max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='sorgulamasonuclari',
            name='soyad',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
