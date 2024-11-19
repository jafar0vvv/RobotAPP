from django.db import models

class SorgulamaSonuclari(models.Model):
    ad = models.CharField(max_length=100, null=True)
    soyad = models.CharField(max_length=100, null=True)
    ata_adi = models.CharField(max_length=100, blank=True, null=True)
    kimlik_seri = models.CharField(max_length=10, null=True)
    kimlik_numarasi = models.CharField(max_length=20, null=True)
    fin_kod = models.CharField(max_length=10, null=True)
    dogum_tarixi = models.DateField(null=True)
    cinsiyet = models.CharField(max_length=10, null=True)
    phone_number = models.CharField(max_length=15, null=True)
    taxes_info = models.TextField(blank=True, null=True)
    emlak_info = models.JSONField(blank=True, null=True)
    infocenter_info = models.JSONField(blank=True, null=True)
    aile_terkibi = models.JSONField(blank=True, null=True)
    abonent_names = models.JSONField(blank=True, null=True)
    mehkeme_result = models.JSONField(blank=True, null=True)
    cinayet_result = models.JSONField(blank=True, null=True)
    inzibati_result = models.JSONField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.ad} {self.soyad} - {self.created_at.strftime('%Y-%m-%d')}"
