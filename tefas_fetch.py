from tefas import Crawler
import pandas as pd
from datetime import datetime, timedelta
import os

def fetch_tefas_data():
    crawler = Crawler()
    
    # === BURAYI KENDİ FON KODLARINLA DEĞİŞTİR ===
    fund_codes = ["AFT", "MAC", "TCD", "IPJ", "YAC"]  # örnek: istediğin kadar ekle
    # =============================================
    
    # Son 365 gün (yaklaşık 1 yıl) veri çekiyoruz
    end_date = datetime.now().strftime("%Y-%m-%d")
    start_date = (datetime.now() - timedelta(days=365)).strftime("%Y-%m-%d")
    
    all_data = []
    for code in fund_codes:
        try:
            # İstediğin kolonları buradan seçebilirsin
            df = crawler.fetch(
                start=start_date,
                end=end_date,
                name=code,
                columns=["code", "title", "date", "price", "market_cap", 
                        "shares_outstanding", "investor_count"]
            )
            all_data.append(df)
            print(f"✅ {code} verisi çekildi ({len(df)} satır)")
        except Exception as e:
            print(f"⚠️ {code} çekilirken hata: {e}")
    
    if all_data:
        combined = pd.concat(all_data, ignore_index=True)
        combined = combined.sort_values(by=["code", "date"]).reset_index(drop=True)
        
        output_file = "tefas_fon_fiyatlari.csv"
        combined.to_csv(output_file, index=False)
        
        print(f"\n🎉 Toplam {len(combined)} satır veri {output_file} dosyasına kaydedildi!")
        print("\nSon fiyatlar (en güncel):")
        latest = combined.groupby("code").last()[["date", "price", "market_cap", "investor_count"]]
        print(latest)
    else:
        print("❌ Hiç veri çekilemedi.")

if __name__ == "__main__":
    fetch_tefas_data()
