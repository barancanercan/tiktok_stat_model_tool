import pandas as pd
from datetime import datetime
import os
import matplotlib
matplotlib.use('Agg')  # GUI gerektirmeyen backend
import matplotlib.pyplot as plt
import seaborn as sns

# Türkçe karakter desteği
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['axes.unicode_minus'] = False


def guncel_veri_girisi():
    csv_dosya_adi = "gonderi_verileri.csv"
    adaylar = ["RTE", "İmamoğlu", "Yavaş", "Özel"]

    standard_columns = (
        ["Başlangıç Tarihi", "Bitiş Tarihi"] +
        [f"{aday} Gönderi Sayısı" for aday in adaylar] +
        [f"{aday} Kümülatif" for aday in adaylar] +
        ["Toplam Kümülatif"] +
        [f"{aday} Kümülatif Oran (%)" for aday in adaylar] +
        [f"{aday} Oran Değişimi (%)" for aday in adaylar]
    )

    # CSV yükle veya yeni oluştur
    if os.path.exists(csv_dosya_adi):
        try:
            df = pd.read_csv(csv_dosya_adi)
            df.columns = [col.strip() for col in df.columns]  # boşlukları temizle

            # Eski sütun adlarını düzelt
            df = df.rename(columns={
                'Başlang': 'Başlangıç Tarihi',
                'Başlangıç': 'Başlangıç Tarihi',
                'İMAMOĞLU Gönderi Sayısı': 'İmamoğlu Gönderi Sayısı',
                'İMAMOĞLU Kümülatif': 'İmamoğlu Kümülatif',
                'İMAMOĞLU Kümülatif Oran (%)': 'İmamoğlu Kümülatif Oran (%)',
                'İMAMOĞLU Oran Değişimi (%)': 'İmamoğlu Oran Değişimi (%)'
            })

            for col in [f"{aday} Gönderi Sayısı" for aday in adaylar]:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0).astype(int)

            df.dropna(how='all', subset=[f"{aday} Gönderi Sayısı" for aday in adaylar], inplace=True)
            df.reset_index(drop=True, inplace=True)

            for col in standard_columns:
                if col not in df.columns:
                    df[col] = 0.0 if "Oran" in col or "Değişim" in col else 0
        except Exception as e:
            print(f"CSV okunamadı: {e}")
            df = pd.DataFrame(columns=standard_columns)
    else:
        df = pd.DataFrame(columns=standard_columns)
        print(f"'{csv_dosya_adi}' bulunamadı. Yeni dosya oluşturulacak.")

    # Kullanıcıdan veri al
    def tarih_al(mesaj):
        while True:
            try:
                t = input(mesaj)
                datetime.strptime(t, "%d.%m.%Y")
                return t
            except ValueError:
                print("Lütfen GG.AA.YYYY formatında girin.")

    baslangic_tarihi = tarih_al("Başlangıç Tarihi (GG.AA.YYYY): ")
    bitis_tarihi = tarih_al("Bitiş Tarihi (GG.AA.YYYY): ")

    try:
        rte = int(input("RTE GÖNDERİ SAYISI: "))
        imamoglu = int(input("İmamoğlu GÖNDERİ SAYISI: "))
        yavas = int(input("Yavaş GÖNDERİ SAYISI: "))
        ozel = int(input("Özel GÖNDERİ SAYISI: "))
    except ValueError:
        print("Tamsayı girilmedi. İşlem iptal.")
        return

    yeni_satir = {
        "Başlangıç Tarihi": baslangic_tarihi,
        "Bitiş Tarihi": bitis_tarihi,
        "RTE Gönderi Sayısı": rte,
        "İmamoğlu Gönderi Sayısı": imamoglu,
        "Yavaş Gönderi Sayısı": yavas,
        "Özel Gönderi Sayısı": ozel
    }

    df = pd.concat([df, pd.DataFrame([yeni_satir])], ignore_index=True)

    for col in standard_columns:
        if col not in df.columns:
            df[col] = 0.0 if "Oran" in col or "Değişim" in col else 0

    # Hesaplamalar
    for aday in adaylar:
        df[f"{aday} Kümülatif"] = df[f"{aday} Gönderi Sayısı"].cumsum()

    df["Toplam Kümülatif"] = df[[f"{aday} Kümülatif" for aday in adaylar]].sum(axis=1)

    for aday in adaylar:
        df[f"{aday} Kümülatif Oran (%)"] = (
            df[f"{aday} Kümülatif"] / df["Toplam Kümülatif"] * 100
        ).replace([float('inf'), -float('inf')], 0).fillna(0).round(2)

    for aday in adaylar:
        oran_col = f"{aday} Kümülatif Oran (%)"
        degisim_col = f"{aday} Oran Değişimi (%)"
        df[degisim_col] = (df[oran_col] - df[oran_col].shift(1)).fillna(0).round(2)
        df.loc[df.index[0], degisim_col] = 0.0

    df.to_csv(csv_dosya_adi, index=False)
    print(f"\n✅ Veriler '{csv_dosya_adi}' dosyasına kaydedildi.")

    # Son satırı göster
    print("\n📊 Son Hafta Verisi:")
    print(df[standard_columns].tail(1).to_string(index=False))

    # Grafikler (PNG'ye kaydet)
    if len(df) > 1:
        df['Bitiş Tarihi_dt'] = pd.to_datetime(df['Bitiş Tarihi'], format="%d.%m.%Y", errors='coerce')
        df.dropna(subset=["Bitiş Tarihi_dt"], inplace=True)

        tarih_etiket = datetime.today().strftime("%Y-%m-%d")

        # Grafik 1: Kümülatif Oran
        plt.figure(figsize=(12, 6))
        for aday in adaylar:
            sns.lineplot(data=df, x="Bitiş Tarihi_dt", y=f"{aday} Kümülatif Oran (%)", label=aday, marker='o')
        plt.title("Kümülatif Oranların Zaman İçindeki Değişimi")
        plt.xlabel("Tarih")
        plt.ylabel("Kümülatif Oran (%)")
        plt.legend()
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(f"kumulatif_oran_grafigi_{tarih_etiket}.png")

        # Grafik 2: Oran Değişimi
        plt.figure(figsize=(12, 6))
        for aday in adaylar:
            sns.lineplot(data=df, x="Bitiş Tarihi_dt", y=f"{aday} Oran Değişimi (%)",
                         label=f"{aday} Değişim", marker='x', linestyle='--')
        plt.title("Kümülatif Oran Değişimi (Haftalık)")
        plt.xlabel("Tarih")
        plt.ylabel("Oran Değişimi (%)")
        plt.legend()
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(f"oran_degisimi_grafigi_{tarih_etiket}.png")

        print(f"\n📈 Grafikler oluşturuldu ve kaydedildi: ")
        print(f" - kumulatif_oran_grafigi_{tarih_etiket}.png")
        print(f" - oran_degisimi_grafigi_{tarih_etiket}.png")


if __name__ == "__main__":
    guncel_veri_girisi()
    print("\n🔁 Yeni veri girişi için programı tekrar çalıştırabilirsiniz.")
