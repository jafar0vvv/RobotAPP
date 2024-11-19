from django.contrib import admin
from django.db import models
from django import forms
import json
from .models import SorgulamaSonuclari

class ReadOnlyAdmin(admin.ModelAdmin):
    readonly_fields = [
        'kimlik_seri', 'kimlik_numarasi', 'fin_kod', 'ad', 'soyad', 'ata_adi',
        'dogum_tarixi', 'cinsiyet', 'phone_number', 'created_at', 'aile_terkibi',
        'mehkeme_result', 'cinayet_result', 'inzibati_result', 'taxes_info', 'emlak_info', 'infocenter_info', 'abonent_names'
    ]

    formfield_overrides = {
        models.JSONField: {
            'widget': forms.Textarea(attrs={'rows': 5, 'cols': 60})
        },
    }

    def get_readonly_fields(self, request, obj=None):
        if not request.user.is_superuser:
            return self.readonly_fields
        return super().get_readonly_fields(request, obj)

    list_display = [
        'ad', 'soyad', 'ata_adi', 'kimlik_seri', 'kimlik_numarasi', 'fin_kod',
        'dogum_tarixi', 'cinsiyet', 'phone_number', 'created_at',
        'display_aile_terkibi', 'display_mehkeme_bilgisi', 'display_cinayet_bilgisi', 'display_inzibati_bilgisi',
        'display_taxes_info', 'display_emlak_info', 'display_infocenter_info', 'display_abonent_names', 
        'display_polis_message'  # Yeni eklenen kolon
    ]

    def display_aile_terkibi(self, obj):
        return self.format_json(obj.aile_terkibi)

    display_aile_terkibi.short_description = 'Aile Terkibi'

    def display_mehkeme_bilgisi(self, obj):
        return self.format_json(obj.mehkeme_result) if hasattr(obj, 'mehkeme_result') else "Veri mevcut değil."

    display_mehkeme_bilgisi.short_description = 'Mahkeme Bilgisi'

    def display_cinayet_bilgisi(self, obj):
        return self.format_json(obj.cinayet_result) if hasattr(obj, 'cinayet_result') else "Veri mevcut değil."

    display_cinayet_bilgisi.short_description = 'Cinayet Bilgisi'

    def display_inzibati_bilgisi(self, obj):
        return self.format_json(obj.inzibati_result) if hasattr(obj, 'inzibati_result') else "Veri mevcut değil."

    display_inzibati_bilgisi.short_description = 'İnzibati Bilgisi'

    def display_taxes_info(self, obj):
        return self.format_text(obj.taxes_info)

    display_taxes_info.short_description = 'Taxes Info'

    def display_emlak_info(self, obj):
        return self.format_text(obj.emlak_info)

    display_emlak_info.short_description = 'Emlak Info'

    def display_infocenter_info(self, obj):
        return self.format_text(obj.infocenter_info)

    display_infocenter_info.short_description = 'Infocenter Info'

    def display_abonent_names(self, obj):
        return self.format_text(obj.abonent_names)

    display_abonent_names.short_description = 'Abonent Names'

    # Yeni fonksiyon ekleniyor
    def display_polis_message(self, obj):
        # Sabit başlık ve metin
        return "POLIS: Axtaris neticeleri tapildi\nBu bölgeye uygun sorgulama sonuçları mevcuttur."

    display_polis_message.short_description = 'POLIS: Axtaris neticeleri tapildi'  # Başlık olarak görünsün

    def format_json(self, json_data):
        """Veriyi formatlayarak okunabilir hale getirir."""
        if not json_data:
            return "Veri mevcut değil."
        try:
            parsed_data = json.loads(json_data)
            if isinstance(parsed_data, dict):
                return json.dumps(parsed_data, indent=4, ensure_ascii=False)
            return json.dumps(parsed_data, indent=4, ensure_ascii=False)
        except (json.JSONDecodeError, TypeError):
            return "Geçersiz JSON verisi"

    def format_text(self, text_data):
        """Metin verilerini düzgün bir şekilde formatlar."""
        if isinstance(text_data, str):
            return text_data.replace("\n", "<br>").replace("\r", "")  # Satır sonlarını HTML <br> etiketiyle değiştirir.
        elif isinstance(text_data, list):
            return "<br>".join([str(item) for item in text_data])  # Liste elemanlarını string'e çevirir
        elif isinstance(text_data, dict):
            # Sözlük verisini düzgün bir metne dönüştürür.
            return "<br>".join([f"{key}: {value}" for key, value in text_data.items()])
        return "Veri mevcut değil."

# Admin sınıfını kaydet
admin.site.register(SorgulamaSonuclari, ReadOnlyAdmin)
