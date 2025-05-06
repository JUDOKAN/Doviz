# Gerekli kütüphaneleri içe aktar
import matplotlib.pyplot as plt
import sqlite3
import os

# -----------------------------------------
# Veritabanından tarih ve fiyat verisini almak için fonksiyon
def get_data(start_date, end_date):
    """
    Belirtilen tarih aralığında USD/TRY verilerini getirir.
    :param start_date: Başlangıç tarihi (str - 'YYYY-MM-DD')
    :param end_date: Bitiş tarihi (str - 'YYYY-MM-DD')
    :return: (tarihler listesi, fiyatlar listesi)
    """
    con = sqlite3.connect('data_Qe2scbv.db')  # Veritabanına bağlan
    cur = con.cursor()
    cur.execute("SELECT * FROM data WHERE date BETWEEN ? AND ? ORDER BY date", (start_date, end_date))
    res = cur.fetchall()
    con.close()

    # Tarih ve fiyat verilerini ayır
    dates = [row[0] for row in res]
    prices = [row[1] for row in res]
    return dates, prices

# -----------------------------------------
# Grafik oluşturan ve dosya olarak kaydeden fonksiyon
def plot_usd_graph(start_date, end_date, save_path='grafikler/usd_tarihsel.png'):
    """
    Verilen tarih aralığında USD/TRY kuru için bir grafik çizer ve kaydeder.
    :param start_date: Başlangıç tarihi
    :param end_date: Bitiş tarihi
    :param save_path: Kaydedilecek grafik dosyasının yolu
    :return: Kaydedilen dosyanın adı
    """
    dates, prices = get_data(start_date, end_date)

    # Grafik boyutu ayarla
    plt.figure(figsize=(12, 6))

    # Çizgi grafiği oluştur
    plt.plot(dates, prices, color='green', linestyle='-', linewidth=2, marker='o', markersize=3)

    # X ekseninde sadece her 100. günü göster
    plt.xticks(ticks=range(0, len(dates), 100), labels=[dates[i] for i in range(0, len(dates), 100)], rotation=45)

    # Grafik başlığı ve etiketler
    plt.title(f"{start_date} - {end_date} Arası USD/TRY Kuru")
    plt.xlabel("Tarih")
    plt.ylabel("USD / TRY")
    plt.grid(True)

    # Grafik klasörü yoksa oluştur
    os.makedirs(os.path.dirname(save_path), exist_ok=True)

    # Grafik dosyasını kaydet
    plt.tight_layout()
    plt.savefig(save_path)

    # Belleği temizle
    plt.close()

    return save_path

# -----------------------------------------
# Örnek test
if __name__ == "__main__":
    # Tarih aralığını belirt (veritabanındaki tarih formatına göre)
    dosya_adi = plot_usd_graph("2021-01-01", "2023-01-01")
    print(f"Grafik başarıyla kaydedildi: {dosya_adi}")
