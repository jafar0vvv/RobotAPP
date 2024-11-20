import json
from django.views import View
import os
from .forms import SorgulamaForm
from .tasks import *
from .models import *
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('sorgulama')  
            else:
                messages.error(request, 'Username veya parol sehvdir.')
        else:
            messages.error(request, 'Uygunsuz giriş melumatlari.')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')  

class FormView(View):
    def get(self, request):
        form = SorgulamaForm()  
        return render(request, 'sorgulama_form.html', {'form': form})



class SorgulamaView(View):
    def post(self, request):
        form = SorgulamaForm(request.POST)  

        if form.is_valid():
            user = request.user
            print(user)
            
            if not user.is_authenticated:
                
                return redirect('login')  
            
            user_data = {
                "kimlik_seri": form.cleaned_data['kimlik_seri'],
                "kimlik_numarasi": form.cleaned_data['kimlik_numarasi'],
                "fin_kod": form.cleaned_data['fin_kod'],
                "ad": form.cleaned_data['ad'],
                "soyad": form.cleaned_data['soyad'],
                "ata_adi": form.cleaned_data['ata_adi'],
                "dogum_tarixi": form.cleaned_data['dogum_tarixi'],
                "cinsiyet": form.cleaned_data['cinsiyet'],
                "phone_number": form.cleaned_data['phone_number']
            }

            emlak_result = emlak_sorgulama(user_data)  
            vergi_result = taxes_sorgulama(user_data)
            hesab_result = hesab_sorgulama(user_data)
            infocenter_result = infocenter_sorgulama(user_data)
            mehkeme_result =  search_in_e_mehkeme(user_data)
            # cerime_result = asanpay_sorgulama(user_data)
            cinayet_result = cinayet_sorgulama(user_data)
            inzibati_result = inzibati_sorgulama(user_data)
            # voen_result = vergi_sorgulama(user_data)
            json_file_path = os.path.join('data', f"{user_data['ad']}_{user_data['soyad']}_results.json") 

            try:
                with open(json_file_path, 'r', encoding='utf-8') as file:
                    data = json.load(file)


                taxes_info = data.get('taxes', {}).get('info', 'Bu melumat movcud deyil.')
                infocenter_info = data.get('infocenter', [])
                emlak_info = data.get('emlak', {})
                aile_terkibi = data.get('aile_terkibi', [])
                abonent_names = data.get('abonent_names', [])
                mehkeme_result = data.get('mehkeme_result', [])
                cinayet_result = data.get('cinayet_result', [])
                inzibati_result = data.get('inzibati_result', [])
                # voen_result = data.get('voen_result', [])
                # cerime_info = data.get('payment_details', [])

                
                emlak_info['Ata_Adı'] = emlak_info.pop('Ata Adı', 'Bu melumat movcud deyil.')
                emlak_info['Doğum_Tarihi'] = emlak_info.pop('Doğum Tarihi', 'Bu melumat movcud deyil.')
                emlak_info['Qeydiyyat_Unvanı'] = emlak_info.pop('Qeydiyyat Ünvanı', 'Bu melumat movcud deyil.')
                emlak_info['ŞV_Seriyası_ve_Numarası'] = emlak_info.pop('ŞV Seriyası ve Numarası', 'Bu melumat movcud deyil.')
                emlak_info['FİN_Kod'] = emlak_info.pop('FİN Kod', 'Bu melumat movcud deyil.')

            except (json.JSONDecodeError, FileNotFoundError) as e:
                taxes_info = "Veri alınamadı."
                infocenter_info = []
                emlak_info = {}
                aile_terkibi = []
                abonent_names = []
                mehkeme_result = []
                inzibati_result = []
                cinayet_result = []
                # voen_result = []

                # cerime_info = []

            # Context oluştur
            context = {
                'taxes_info': taxes_info,
                'emlak_info': emlak_info,
                'infocenter_info': infocenter_info,
                'aile_terkibi': aile_terkibi,
                'abonent_names': abonent_names,
                'mehkeme_result': mehkeme_result,
                'cinayet_result':cinayet_result,
                'inzibati_result':inzibati_result,
                # 'voen_result':voen_result,
                # 'cerime_info' : cerime_info
            }


            SorgulamaSonuclari.objects.create(
                ad=user_data['ad'],
                soyad=user_data['soyad'],
                ata_adi=user_data['ata_adi'],
                kimlik_seri=user_data['kimlik_seri'],
                kimlik_numarasi=user_data['kimlik_numarasi'],
                fin_kod=user_data['fin_kod'],
                dogum_tarixi=user_data['dogum_tarixi'],
                cinsiyet=user_data['cinsiyet'],
                phone_number=user_data['phone_number'],
                taxes_info=taxes_info,
                emlak_info=emlak_info,
                infocenter_info=infocenter_info,
                aile_terkibi=aile_terkibi,
                abonent_names=abonent_names,
                mehkeme_result=mehkeme_result,
                cinayet_result=cinayet_result,
                inzibati_result=inzibati_result,
                # voen_result = voen_result
            )
           
            return render(request, 'sorgulama_sonuclari.html', context)






