import json
import undetected_chromedriver as uc
from twocaptcha import TwoCaptcha
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
from datetime import datetime
from selenium import webdriver
from datetime import date
from selenium.webdriver.common.action_chains import ActionChains
import requests
import base64
from selenium.common.exceptions import TimeoutException, ElementNotInteractableException
from selenium.common.exceptions import StaleElementReferenceException
API_KEY = "bfa56f4a2e56c1d1e9b5044e3e1109c4"

web_eemlak = "https://e-emlak.gov.az/eemdk/services/mobile/login"
web_infocenter = "https://www.infocenter.gov.az/e-services/adsoyad.aspx"
web_taxes = "https://www.taxes.gov.az/az/page/olkeden-getmek-huququnun-muveqqeti-mehdudlasdirilmasi"
web_hesab = "https://hesab.az/unregistered/#/direct-pay/telephone/generalrabita/parameters" 
web_cerime = "https://www.asanpay.az/intro/home#"
web_e_mehkeme = "https://e-mehkeme.gov.az/Public/Cases"
web_mehkeme = "https://sc.supremecourt.gov.az/job/search/2"

final_results = {
    "taxes": [],
    "infocenter": [],
    "emlak": {},
    "aile_terkibi": []
    
}

def get_user_data(form_data):
    return {
        "kimlik_seri": form_data.get("kimlik_seri", ""),
        "kimlik_numarasi": form_data.get("kimlik_numarasi", ""),
        "fin_kod": form_data.get("fin_kod", ""),
        "ad": form_data.get("ad", ""),
        "soyad": form_data.get("soyad", ""),
        "ata_adi": form_data.get("ata_adi", ""),
        "dogum_tarixi": form_data.get("dogum_tarixi", ""),
        "cinsiyet": form_data.get("cinsiyet", ""),
        "phone_number": form_data.get("phone_number", "")
    }


def get_json_file_name(user_data):
    base_name = f"{user_data['ad']}_{user_data['soyad']}_results"
    return os.path.join('data', f"{base_name}.json")

def save_results_to_json(data, user_data):
    json_file = get_json_file_name(user_data)
    os.makedirs(os.path.dirname(json_file), exist_ok=True)

    if os.path.exists(json_file):
        with open(json_file, 'r', encoding='utf-8') as existing_file:
            existing_data = json.load(existing_file)
        existing_data.update(data)
        data = existing_data  

    
    with open(json_file, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)

    print(f"{json_file} kaydedildi.")

def solve_recaptcha(driver):
    try:
        print("reCAPTCHA iframe loading ...")
        reCAPTCHA_iframe = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//iframe[contains(@src, 'recaptcha')]"))
        )
        driver.switch_to.frame(reCAPTCHA_iframe)
        sitekey = "6Le-wvkSAAAAAPBMRTvw0Q4Muexq9bi0DJwx_mJ-"
        return sitekey
    except Exception as e:
        print(f"iframe yükleme hatası: {str(e)}")
    finally:
        driver.switch_to.default_content()
    return None

def emlak_sorgulama(user_data):
    options = uc.ChromeOptions()
    options.add_argument('--headless')
    driver = uc.Chrome(options=options)
    driver.get(web_eemlak)

    try:
        driver.find_element(By.CLASS_NAME, 'ant-select-selector').click()
        time.sleep(1)

        kimlik_seri_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, f'//div[@title="{user_data["kimlik_seri"]}"]'))
        )
        kimlik_seri_element.click()

        driver.find_element(By.NAME, 'SerialNumber').send_keys(user_data["kimlik_numarasi"])
        driver.find_element(By.NAME, 'Pin').send_keys(user_data["fin_kod"])

        sitekey = solve_recaptcha(driver)

        if sitekey:
            solver = TwoCaptcha(API_KEY)
            print("CAPTCHA passing...")
            response = solver.recaptcha(sitekey=sitekey, url=web_eemlak)

            if "code" in response:
                print(f'CAPTCHA Anahtarı: {response["code"]}')
                driver.execute_script("document.getElementById('g-recaptcha-response').value = '{}';".format(response["code"]))
                
                try:
                    daxil_ol_button = driver.find_element(By.XPATH, '//button[contains(@class, "btn-login")]/span[text()="Daxil ol"]')
                    daxil_ol_button.click()
                    print("Daxil ol butonuna tıklandı.")

                    # Emlak bilgilerini almak için bekle
                    ad_element = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, '//label[b[contains(text(), "Ad")]]/parent::div/following-sibling::div//input'))
                    )
                    ad = ad_element.get_attribute('value')
                    print(f"Ad: {ad}")  # Ad değerini kontrol et

                    soyad_element = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, '//label[b[contains(text(), "Soyad")]]/parent::div/following-sibling::div//input'))
                    )
                    soyad = soyad_element.get_attribute('value')
                    print(f"Soyad: {soyad}")  # Soyad değerini kontrol et

                    ata_ad_element = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, '//label[b[contains(text(), "Ata adı")]]/parent::div/following-sibling::div//input'))
                    )
                    ata_ad = ata_ad_element.get_attribute('value')
                    print(f"Ata Adı: {ata_ad}")  # Ata Adı değerini kontrol et

                    dogum_tarihi_element = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, '//label[b[contains(text(), "Doğum Tarixi")]]/parent::div/following-sibling::div//input'))
                    )
                    dogum_tarihi = dogum_tarihi_element.get_attribute('value')
                    print(f"Doğum Tarihi: {dogum_tarihi}")  # Doğum Tarihi değerini kontrol et

                    qeydiyyat_element = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, '//label[b[contains(text(), "Qeydiyyat ünvanı")]]/parent::div/following-sibling::div//input'))
                    )
                    qeydiyyat = qeydiyyat_element.get_attribute('value')
                    print(f"Qeydiyyat Ünvanı: {qeydiyyat}")  # Qeydiyyat Ünvanı değerini kontrol et

                    sv_element = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, '//label[b[contains(text(), "ŞV seriya və nömrəsi:")]]/parent::div/following-sibling::div//input'))
                    )
                    sv = sv_element.get_attribute('value')
                    print(f"ŞV Seriyası ve Numarası: {sv}")  # ŞV Seriyası ve Numarası değerini kontrol et

                    fin_element = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, '//label[b[contains(text(), "FİN kod:")]]/parent::div/following-sibling::div//input'))
                    )
                    fin = fin_element.get_attribute('value')
                    print(f"FİN Kod: {fin}")  # FİN Kod değerini kontrol et

                    final_results["emlak"] = {
                        "Ad": ad,
                        "Soyad": soyad,
                        "Ata Adı": ata_ad,
                        "Doğum Tarihi": dogum_tarihi,
                        "Qeydiyyat Ünvanı": qeydiyyat,
                        "ŞV Seriyası ve Numarası": sv,
                        "FİN Kod": fin,
                    }
                    print("Emlak bilgileri başarıyla alındı.")

                    # final_results içeriğini kontrol et
                    print(f"Final Results: {final_results}")  

                    if final_results["emlak"]:
                        save_results_to_json(final_results, user_data)
                        print("Emlak bilgileri JSON dosyasına kaydedildi.")
                    return final_results["emlak"]
                except Exception as e:
                    print(f"Emlak bilgilerini alma hatası: {e}")
            else:
                print("CAPTCHA hatası.")
        else:
            print("reCAPTCHA hatası.")

    except Exception as e:
        print(f"Emlak sorgulama hatası: {e}")
    finally:
        driver.quit()

def taxes_sorgulama(user_data):
    options = uc.ChromeOptions()
    options.add_argument('--headless')
    driver = uc.Chrome(options=options)
    driver.get(web_taxes)
    
    try:
        iframe = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.ID, "iFrameId"))
        )
        driver.switch_to.frame(iframe)
        print("İframe'e geçiş yapıldı.")

        fin_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "fin-input"))
        )
        fin_input.send_keys(user_data["fin_kod"])
        print("Fin kodu girildi.")

        yoxla_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "yoxla"))
        )
        yoxla_button.click()
        print("YOXLA butonuna tıklandı.")

        result_section = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "modal-content"))
        )
        result = result_section.text

        try:
            final_results["taxes"] = json.loads(result)  # JSON formatındaysa sözlük olarak ekle
        except json.JSONDecodeError:
            final_results["taxes"] = {"info": result}  # JSON değilse, düz metin olarak ekle

        print("Vergi bilgileri başarıyla alındı.")
        
        # Vergi bilgilerini JSON dosyasına kaydet
        save_results_to_json(final_results, user_data)
        print("Vergi bilgileri JSON dosyasına kaydedildi.")

        return final_results["taxes"]

    except Exception as e:
        print(f"Vergi sorgulama hatası: {e}")
    finally:
        driver.quit()


def aile_terkibi(daire_id, mentqe_id, soyad, secici_unvani,user_data):
    """CAPTCHA çözümleme ve Davam et butonuna tıklama işlemini gerçekleştirir."""
    options = uc.ChromeOptions()
    driver = uc.Chrome(options=options)
    driver.set_window_size(250, 100)  # Yalnızca CAPTCHA alanını görecek şekilde ayar
    driver.set_window_position(800, 400)   # Pencereyi ekranın istediğiniz bir konumuna yerleştirin.
    final_results = {"aile_terkibi": []}  # Bu satır eklendi

    try:
        driver.get(f"https://www.infocenter.gov.az/page/voters/?s={daire_id}&sm={mentqe_id}")
        print(f"{daire_id} ve {mentqe_id} ile yeni sayfaya geçiliyor...")

        # Sayfanın tamamen yüklendiğinden emin ol
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        print("Yeni sayfa yüklendi.")

        # CAPTCHA'yı çözmeniz için bilgilendirme
        print("Lütfen CAPTCHA'yı çözün ve ardından 'Davam et' butonuna tıklayın.")

        # CAPTCHA'nın çözülmesi için bekleme zamanı
        # Bu sırada butona kendiniz tıklayacaksınız
        WebDriverWait(driver, 300).until_not(EC.visibility_of_element_located((By.XPATH, "//span[text()='Davam et']")))
        print("Davam et butonuna tıklama algılandı, işlemler devam ediyor...")

        # Sonuç tablosunun yüklenmesini bekle
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '//tbody/tr')))
        print("Sonuç tablosu yüklendi.")

        new_data = []
        rows = driver.find_elements(By.XPATH, '//tr[contains(@align, "center")]')

        soyad_prefix = soyad[:3].upper()
        secici_unvani_prefix = secici_unvani.rsplit(",", 1)[0].strip()

        print("İlk 3 harfli soyad:", soyad_prefix)
        print("Virgülden önceki unvan:", secici_unvani_prefix)

        for row in rows:
            columns = row.find_elements(By.TAG_NAME, "td")
            if columns:
                secici_ad_soyad = columns[2].text.strip()  # Ad soyadı 0. sütunda
                if secici_ad_soyad.startswith(soyad_prefix) and columns[3].text.strip().startswith(secici_unvani_prefix):
                    data = {
                        "dairenin_kodu": columns[0].text.strip(),
                        "mentqenin_kodu": columns[1].text.strip(),
                        "secicinin_soyadi_adi": secici_ad_soyad,
                        "yasayis_yeri": columns[3].text.strip(),
                        "tevellud": columns[4].text.strip(),
                    }
                    new_data.append(data)
                    final_results["aile_terkibi"].append(data)  # aile_terkibi sonuçlarına ekleme

        if new_data:
            save_results_to_json(final_results,user_data)  # user_data gerek yok
            print("Yeni veriler başarıyla kaydedildi.")
            print(new_data)
        else:
            print("Searching failed: No results found.")

    except Exception as e:
        print(f"Aile terkibi sorgulama hatası: {e}")
    finally:
        driver.quit()

# JSON'a yazmak için kullanılacak fonksiyon
def infocenter_sorgulama(user_data):
    """İnfocenter sorgulama işlemini gerçekleştirir."""
    options = uc.ChromeOptions()
    # options.add_argument('--headless')
    driver = uc.Chrome(options=options)
    driver.get(web_infocenter)

    final_results = {
        "infocenter": []
    }

    try:
        driver.find_element(By.CSS_SELECTOR, '[id="ctl00_HolderBody_TxtSoyad_I"]').send_keys(user_data["soyad"])
        driver.find_element(By.CSS_SELECTOR, '[id="ctl00_HolderBody_TxtAd_I"]').send_keys(user_data["ad"])
        driver.find_element(By.CSS_SELECTOR, '[id="ctl00_HolderBody_TxtAtaAdi_I"]').send_keys(user_data["ata_adi"])

        if isinstance(user_data["dogum_tarixi"], date):
            dogum_tarihi_str = user_data["dogum_tarixi"].strftime('%d.%m.%Y')
        else:
            dogum_tarihi_str = user_data["dogum_tarixi"]

        dogum_tarihi_elem = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[id="ctl00_HolderBody_tevelllud_I"]')))
        dogum_tarihi_elem.clear()
        dogum_tarihi_elem.send_keys(dogum_tarihi_str)

        cinsiyet_input = driver.find_element(By.ID, 'ctl00_HolderBody_CboxCins_I') 
        cinsiyet_input.click() 
        if user_data["cinsiyet"].lower() == "kişi": 
            male_option = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[id="ctl00_HolderBody_CboxCins_DDD_L_LBI0T1"]')))
            male_option.click() 
        elif user_data["cinsiyet"].lower() == "qadın": 
            female_option = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[id="ctl00_HolderBody_CboxCins_DDD_L_LBI1T1"]'))) 
            female_option.click() 

        search_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//div[@id="ctl00_HolderBody_BtnSearch_CD"]/span[text()="Axtar"]')))
        search_button.click()  

        table = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.ID, 'ctl00_HolderBody_GridNetice')))
        rows = table.find_elements(By.TAG_NAME, "tr")
        
        for row in rows[1:]:
            columns = row.find_elements(By.TAG_NAME, "td")
            if columns:  
                data = {
                    "ad_soyad_ata_adi": columns[0].text.strip(),
                    "daire_ve_unvani": columns[1].text.strip(),
                    "dairenin_marsrutu": columns[2].text.strip(),
                    "mentqenin_unvani": columns[3].text.strip(),
                    "mentqenin_marsrutu": columns[4].text.strip(),
                    "secicinin_unvani": columns[5].text.strip(),
                }
                final_results["infocenter"].append(data)
        print(final_results["infocenter"]) 

        if final_results["infocenter"]:
            save_results_to_json(final_results, user_data)
            print("Infocenter bilgileri JSON dosyasına kaydedildi.")

        if rows:
            first_row_columns = rows[1].find_elements(By.TAG_NAME, "td")
            if len(first_row_columns) > 5:
                daire_id = first_row_columns[1].text.split()[0].strip()
                mentqe_id = first_row_columns[3].text.split()[0].strip()
                soyad = user_data["soyad"]
                secici_unvani = first_row_columns[5].text.strip()

                aile_terkibi(daire_id, mentqe_id, soyad, secici_unvani, user_data)
            else:
                print("Beklenenden az sütun mevcut. İlk satırda veri eksikliği olabilir.")
        else:
            print("Infocenter'da sonuç bulunamadı.")
    except Exception as e:
        print(f"Infocenter sorgulama hatası: {e}")
    finally:
        driver.quit()



def hesab_sorgulama(user_data):
    options = uc.ChromeOptions()
    options.add_argument('--headless')  # Headless (görünmez) mod
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    driver = uc.Chrome(options=options)
    driver.get(web_hesab)

    final_results = {}

    try:
        # Telefon numarasını bul ve bir değer gir
        number_input = WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='number']"))
        )
        number_input.send_keys(user_data["phone_number"])  # Telefon numarasını gir

        # "Davam et" butonunu bul ve tıkla
        continue_button = WebDriverWait(driver, 60).until(
            EC.element_to_be_clickable((By.ID, "generalrabita_parametrs"))
        )
        continue_button.click()

        # Abonent isimlerini alma
        abonent_name_elements = WebDriverWait(driver, 60).until(
            EC.presence_of_all_elements_located((By.XPATH, "//li[@class='label-part ng-star-inserted']//span"))
        )
        abonent_names = [element.text.strip() for element in abonent_name_elements if element.text.strip()]  # Boş isimleri filtrele
        final_results["abonent_names"] = abonent_names  # Sonuçlara ekle

        # Abonent isimlerini yazdır
        for name in abonent_names:
            print(f"Abonent: {name}")  # Abonent ismini yazdır

        print("Abonent adları alındı:", abonent_names)
        if abonent_names:
            save_results_to_json(final_results, user_data)
            print("Abonent bilgileri JSON dosyasına kaydedildi.")
        return final_results
    except Exception as e:
        print(f"Hesab sorgulama hatası: {e}")
    finally:
        driver.quit()


def search_in_e_mehkeme(user_data):
    options = uc.ChromeOptions()
    options.add_argument('--headless')  # Tarayıcıyı görünmez çalıştırır
    options.add_argument('--disable-gpu')  # GPU'yu devre dışı bırakır, bazı sistemlerde headless modda gerekli
    options.add_argument('--no-sandbox')  # Daha kararlı çalışması için
    options.add_argument('--disable-dev-shm-usage')  # Paylaşılan hafızayı devre dışı bırakır, özellikle Linux için

    driver = uc.Chrome(options=options)
    driver.get("https://example.com")  # URL doğru olmalı

    try:
        # Axtarış butonuna tıklama
        search_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.ID, "PublicSearch"))
        )
        search_button.click()

        # FIN kodu giriş alanını doldurma
        if user_data.get("fin_kod"):
            try:
                fin_input = WebDriverWait(driver, 20).until(
                    EC.visibility_of_element_located((By.ID, "DocFin"))
                )
                driver.execute_script("arguments[0].scrollIntoView(true);", fin_input)
                fin_input.clear()
                fin_input.send_keys(user_data["fin_kod"])
            except StaleElementReferenceException:
                fin_input = WebDriverWait(driver, 20).until(
                    EC.visibility_of_element_located((By.ID, "DocFin"))
                )
                fin_input.clear()
                fin_input.send_keys(user_data["fin_kod"])

        # Axtar butonuna tıklama
        axtar_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.ID, "btnSearch"))
        )
        axtar_button.click()

        # Sonuçların yüklenmesini bekleme
        result_element = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//div[@class='pagination-container']//a"))
        )
        result_text = result_element.text.strip()

        if "(0 iş)" in result_text:
            result_message = "Qeydiyyatda olan məhkəmə işi tapılmamışdır."
        else:
            # Tabloyu bekleyelim
            case_table = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.ID, "Cases"))
            )

            # Tabloyu kontrol et ve satırları al
            rows = case_table.find_elements(By.TAG_NAME, "tr")[1:]  # Başlık satırını atla

            if not rows:  # Satırlar boşsa hata mesajı ver
                print("No rows found in the case table.")
                return {"error": "Tabloda veri bulunamadı."}

            case_details = []
            for row in rows:
                columns = row.find_elements(By.TAG_NAME, "td")

                # Yeterli hücre olup olmadığını kontrol et
                if len(columns) < 6:  # Satırda 6 hücre bekliyoruz
                    print("Satırda yeterli hücre bulunamadı:", row.text)
                    continue  # Bu satırı atla

                case_info = {
                    "işin nömrəsi": columns[0].text.strip(),
                    "daxil olma tarixi": columns[1].text.strip(),
                    "işin növü": columns[2].text.strip(),
                    "məhkəmənin adı": columns[3].text.strip(),
                    "hakim": columns[4].text.strip(),
                    "işin baxılma vəziyyəti": columns[5].text.strip(),
                }
                case_details.append(case_info)
            result_message = case_details

        # Sonuçları JSON'a kaydet
        final_results = {"mehkeme_result": result_message}
        save_results_to_json(final_results, user_data)
        return result_message

    except TimeoutException as e:
        print("Sayfa yüklenemedi veya sonuç bulunamadı:", e)
        return {"error": "Sayfa yüklenemedi veya sonuç bulunamadı."}

    except ElementNotInteractableException as e:
        print("Elementle etkileşim kurulamadı:", e)
        return {"error": "Elementle etkileşim kurulamadı."}

    finally:
        driver.quit()
def clean_result_text(result_text):
    if "(" in result_text and ")" in result_text:
        return result_text.split("(")[0].strip()  # Parantezden önceki kısmı döndür
    return result_text.strip() 


def asanpay_sorgulama(user_data):
    options = uc.ChromeOptions()
    # options.add_argument('--headless')  # Headless (görünmez) mod
    # options.add_argument('--no-sandbox')
    # options.add_argument('--disable-dev-shm-usage')
    
    driver = uc.Chrome(options=options)
    driver.get(web_cerime)

    final_results = {}

    try:
        # "Daxili İşlər Nazirliyi" seçeneğine tıklama
        din_element = WebDriverWait(driver, 60).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "nav.text-center.m-auto"))
        )
        din_element.click()

        # "FİN və seriya nömrəsi ilə axtarış" seçeneğine tıklama
        search_option = WebDriverWait(driver, 60).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "li.select2-results__option--highlighted"))
        )
        search_option.click()

        # FIN numarasını girme
        fin_input = WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='pin']"))
        )
        fin_input.send_keys(user_data["fin"])  # Formdan gelen FIN numarasını gir

        # "Axtar" butonuna tıklama
        search_button = WebDriverWait(driver, 60).until(
            EC.element_to_be_clickable((By.ID, "searchPaymentByIdentificationType"))
        )
        search_button.click()

        # Sayfadan gerekli bilgileri alma
        payment_elements = WebDriverWait(driver, 60).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "li.list-group-item"))
        )

        # Ödeme detaylarını alma
        payment_details = {}
        for element in payment_elements:
            label = element.find_element(By.TAG_NAME, "h6").text.strip()
            value = element.find_element(By.CLASS_NAME, "mb-0").text.strip()
            payment_details[label] = value
        
        final_results["payment_details"] = payment_details  # Sonuçlara ekle

        # Ödeme detaylarını yazdır
        for label, value in payment_details.items():
            print(f"{label} {value}")

        print("Ödeme detayları alındı:", payment_details)
        if payment_details:
            save_results_to_json(final_results, user_data)
            print("Abonent bilgileri JSON dosyasına kaydedildi.")
        return final_results

    except Exception as e:
        print(f"Asanpay sorgulama hatası: {e}")
    finally:
        driver.quit()

def cinayet_sorgulama(user_data):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    driver.get("https://sc.supremecourt.gov.az/job/search/1")
    
    try:
        # Soyad, Ad, ve Ata adı alanlarını doldur
        soyad_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "search_adv_form_first_name"))
        )
        soyad_input.send_keys(user_data["soyad"])
        print("Soyad girildi.")

        ad_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "search_adv_form_name"))
        )
        ad_input.send_keys(user_data["ad"])
        print("Ad girildi.")

        ata_adi_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "search_adv_form_last_name"))
        )
        ata_adi_input.send_keys(user_data["ata_adi"])
        print("Ata adı girildi.")

        # 'Axtar' butonuna tıklama
        axtar_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn.btn-info.pull-right"))
        )
        axtar_button.click()
        print("Axtar butonuna tıklandı.")

        # Sonuçları bekleyin ve "Tapılmadı" kontrolünü yapın
        try:
            not_found_message = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "//p[@align='center' and contains(text(), 'Tapılmadı')]"))
            )
            print("Tapılmadı mesajı bulundu.")
        except:
            # Tapılmadı mesajı yoksa diğer sonuçları alın
            result_section = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.CLASS_NAME, "col-md-9"))
            )
            result_text = result_section.text
            result_text = "Cinayət tərkib məkhəməsi yoxdur"
            print("Sonuç bilgileri alındı:", result_text)

        # Sonucu JSON olarak kaydet
        final_results = {"cinayet_result": result_text}
        save_results_to_json(final_results, user_data)
        print("Sonuçlar JSON dosyasına kaydedildi.")

        return final_results["cinayet_result"]

    except Exception as e:
        print(f"Supreme Court sorgulama hatası: {e}")
    finally:
        driver.quit()


def inzibati_sorgulama(user_data):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Tarayıcıyı başlatmadan çalıştırmak için
    driver = webdriver.Chrome(options=options)
    driver.get("https://sc.supremecourt.gov.az/job/search/2-1")

    try:
        # Soyad, Ad, ve Ata adı alanlarını doldur
        soyad_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "search_adv_form_first_name"))
        )
        soyad_input.send_keys(user_data["soyad"])
        print("Soyad girildi.")

        ad_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "search_adv_form_name"))
        )
        ad_input.send_keys(user_data["ad"])
        print("Ad girildi.")

        ata_adi_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "search_adv_form_last_name"))
        )
        ata_adi_input.send_keys(user_data["ata_adi"])
        print("Ata adı girildi.")



        # 'Axtar' butonuna tıklama
        axtar_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn.btn-info.pull-right"))
        )
        axtar_button.click()
        print("Axtar butonuna tıklandı.")

        # Sonuçları bekleyin ve "Tapılmadı" kontrolünü yapın
        try:
            not_found_message = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "//p[@align='center' and contains(text(), 'Tapılmadı')]"))
            )
            print("Tapılmadı mesajı bulundu.")
        except:
            # Tapılmadı mesajı yoksa diğer sonuçları alın
            result_section = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.CLASS_NAME, "col-md-9"))
            )
            result_text = result_section.text
            result_text = "Inzibati tərkib məkhəməsi yoxdur"

            print("Sonuç bilgileri alındı:", result_text)

        # Sonucu JSON olarak kaydet
        final_results = {"inzibati_result": result_text}
        save_results_to_json(final_results, user_data)
        print("Sonuçlar JSON dosyasına kaydedildi.")

        return final_results["inzibati_result"]

    except Exception as e:
        print(f"Supreme Court sorgulama hatası: {e}")
    finally:
        driver.quit()

def main(form_data):
    user_data = get_user_data(form_data)
    final_results = {}
    
    # Sorgulama işlemleri
    final_results["emlak"] = emlak_sorgulama(user_data)
    final_results["taxes"] = taxes_sorgulama(user_data)
    final_results["infocenter"] = infocenter_sorgulama(user_data)
    final_results["aile_terkibi"] = aile_terkibi(user_data)
    final_results["abonent_name"] = hesab_sorgulama(user_data)
    # Sonuçları JSON dosyasına kaydet
    save_results_to_json(final_results, user_data)  # Sıralama düzeltildi
    
if __name__ == "__main__":
    form_data = {}  # Burada gerçek form verilerini geçin
    main(form_data)


