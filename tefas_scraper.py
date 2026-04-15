import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime

# Çekmek istediğiniz fon kodlarını buraya yazın
FON_LISTESI = ["TMG", "MAC", "AFT", "YAS", "NNF"]

def get_fon_price(fon_kod):
    fon_kod = fon_kod.upper()
    url = f"https://www.tefas.gov.tr/FonAnaliz.aspx?FonKod={fon_kod}"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status() 
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Fiyatı yakalama
        price_element = soup.select_one('ul.top-list li span')
        
        if price_element:
            price_str = price_element.text.strip()
            formatted_price = price_str.replace('.', '').replace(',', '.')
            return float(formatted_price)
        else:
            return "Bulunamadı"

    except Exception as e:
        return f"Hata"

def main():
    # Günün tarihini al (Örn: 2024-03-15)
    tarih = datetime.now().strftime("%Y-%m-%d")
    
    # CSV dosyasını oluştur / üzerine yaz
    # Not: Her gün sadece güncel veriyi istiyorsanız 'w' (write), 
    # geçmişi de tutmak istiyorsanız 'a' (append) kullanın. 
    # Spreadsheet'e son durumu çekeceğimiz için 'w' kullanıyoruz.
    with open('fon_fiyatlari.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        # Başlıkları yaz
        writer.writerow(['Tarih', 'Fon Kodu', 'Fiyat'])
        
        # Fonları dön ve fiyatları kaydet
        for fon in FON_LISTESI:
            print(f"{fon} çekiliyor...")
            fiyat = get_fon_price(fon)
            writer.writerow([tarih, fon, fiyat])
            
    print("İşlem tamamlandı, CSV oluşturuldu.")

if __name__ == "__main__":
    main()
