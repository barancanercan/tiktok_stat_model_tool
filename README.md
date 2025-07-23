# Gönderi Verileri Takip ve Analiz Aracı

Bu Python kodu, belirli adayların sosyal medya gönderi sayılarını haftalık olarak takip etmek, kümülatif istatistikleri hesaplamak ve zaman içindeki oran değişimlerini grafiksel olarak görselleştirmek için geliştirilmiştir.

---

## 📌 Özellikler

* Haftalık gönderi verisi girişi (manuel olarak terminalden).
* CSV dosyası üzerinden verilerin saklanması ve güncellenmesi.
* Aday bazlı kümülatif gönderi sayısı, toplam oran ve haftalık değişim hesaplaması.
* Zaman serisine dayalı çizgi grafik üretimi (otomatik olarak `.png` formatında kaydedilir).
* Türkçe karakter uyumlu grafik üretimi.

---

## ⚙️ Kurulum

### 1. Gereksinimler

* Python 3.8 veya üzeri
* Aşağıdaki Python kütüphaneleri:

  ```bash
  pip install pandas matplotlib seaborn
  ```

### 2. (Opsiyonel) Sanal Ortam Kurulumu

```bash
python3 -m venv .venv
source .venv/bin/activate  # Windows için: .venv\Scripts\activate
pip install pandas matplotlib seaborn
```

---

## ▶️ Kullanım

### 1. Betiği çalıştırın:

```bash
python main.py
```

### 2. İstenen verileri girin:

* Başlangıç ve bitiş tarihi (GG.AA.YYYY formatında)
* Her aday için gönderi sayısı (tam sayı)

### 3. Çıktılar:

* `gonderi_verileri.csv`: Verilerin saklandığı dosya
* `kumulatif_oran_grafigi_YYYY-MM-DD.png`: Kümülatif oran zaman grafiği
* `oran_degisimi_grafigi_YYYY-MM-DD.png`: Haftalık oran değişim grafiği

---

## 🧾 CSV Dosyası Formatı

Betik, aşağıdaki başlıklara sahip bir CSV dosyasını kullanır veya otomatik olarak oluşturur:

```csv
Başlangıç Tarihi,Bitiş Tarihi,RTE Gönderi Sayısı,İmamoğlu Gönderi Sayısı,Yavaş Gönderi Sayısı,Özel Gönderi Sayısı
```

* Tarih formatı: `GG.AA.YYYY`
* Dosyada büyük harfli başlıklar ya da fazla sütun varsa, betik düzeltmeye çalışır.

---

## 📊 Üretilen Grafikler

1. **Kümülatif Oran Grafiği**
   Adayların gönderi sayılarının toplam içindeki oranlarının zaman içindeki değişimi.

2. **Oran Değişimi Grafiği**
   Adayların haftalık kümülatif oran değişim yüzdeleri.

Grafikler `.png` formatında otomatik olarak bulunduğunuz dizine kaydedilir.

---

## 🛠 Sorun Giderme

| Sorun                                            | Çözüm                                                                              |
| ------------------------------------------------ | ---------------------------------------------------------------------------------- |
| Grafik görünmüyor                                | Grafikler `plt.savefig(...)` ile `.png` olarak kaydedilir, terminalde gösterilmez. |
| Hatalı tarih girdisi                             | Format: `GG.AA.YYYY` (örn. `05.07.2025`)                                           |
| CSV hataları                                     | Başlıklar eksik veya bozuksa betik otomatik olarak düzeltmeye çalışır.             |

---

## 🤝 Katkıda Bulunma

Her türlü katkı, öneri veya hata bildirimi için PR (pull request) veya issue açabilirsiniz.

---

## 📄 Lisans

Bu proje açık kaynaklıdır. Dilediğiniz gibi kullanabilir, geliştirebilir veya paylaşabilirsiniz.


