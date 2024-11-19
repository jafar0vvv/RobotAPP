from django import forms

class SorgulamaForm(forms.Form):
    kimlik_seri = forms.CharField(max_length=3,required=False)
    kimlik_numarasi = forms.CharField(max_length=8,required=False)
    fin_kod = forms.CharField(max_length=7,required=False)
    ad = forms.CharField(max_length=50,required=False)
    soyad = forms.CharField(max_length=50,required=False)
    ata_adi = forms.CharField(max_length=50,required=False)
    dogum_tarixi = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'text', 'placeholder': 'DD.MM.YYYY'}),
        input_formats=['%d.%m.%Y'],required=False  # Formdan gelen tarih formatını belirliyoruz.
    )
    cinsiyet = forms.ChoiceField(choices=[('kişi', 'Kişi'), ('qadın', 'Qadın')],required=False)
    phone_number = forms.CharField(max_length=10,required=False)