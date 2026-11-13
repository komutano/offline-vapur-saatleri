# Offline Vapur Saatleri ⛴️

İnternet bağlantısı gerektirmeden çalışan vapur saatleri uygulaması.

**Önemli Notlar:**
* ⚠️ **Uyumluluk:** Bu uygulama **sadece iOS Pythonista** uygulamasında test edilmiştir. İçerdiği arayüz (`ui`) modülü Pythonista'ya özeldir, standart bilgisayar ortamlarında (Windows/Mac) doğrudan çalışmaz.
* 📍 **Kapsam:** Bu veritabanı sadece **Karaköy <-> Kadıköy** hattında hizmet veren **Şehir Hatları** ve **Turyol** firmalarının sefer saatlerini içermektedir. Diğer güzergahlar mevcut değildir.

## Özellikler
* **Tamamen Çevrimdışı:** Veriler `vapur_verisi.py` içinde tutulur, API veya internet bağlantısı gerektirmez.
* **Akıllı Saat Hesaplama:** Bulunduğunuz saate göre sıradaki en yakın 2 seferi otomatik gösterir.
* **Gün Takibi:** Hafta içi, Cumartesi ve Pazar günlerine göre otomatik tarife seçimi.
* **Çoklu Firma Desteği:** Şehir Hatları ve Turyol seferlerini aynı ekranda karşılaştırmalı sunar.

## Kurulum ve Kullanım (Pythonista)
1. Bu depodaki `vapur_verisi.py` ve `vapur_saatleri.py` dosyalarını iOS cihazınızdaki Pythonista uygulamasına indirin (ikisi aynı klasörde olmalı).
2. `vapur_saatleri.py` dosyasını açıp çalıştırın (Play butonu).
3. Ekranda beliren arayüzden kalkış yönünüzü seçerek sıradaki seferleri görebilirsiniz.
