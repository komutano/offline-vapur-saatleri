"""
vapur_saatleri.py
Kadıköy <-> Karaköy vapur saatleri (Şehir Hatları + Turyol)
Pythonista arayüzü - GÜNCEL VERSİYON

Bu dosya, vapur_verisi.py dosyasındaki verileri okuyarak
kullanıcıya en yakın iki vapur seferini gösterir.
"""

import ui
import datetime
from vapur_verisi import VERI_HAVUZU  # Veritabanımız

def time_str_to_minutes(t):
    """'SS:DD' formatındaki saati, günün başından itibaren geçen dakika cinsine çevirir."""
    h, m = t.split(':')
    return int(h) * 60 + int(m)

def get_next_departures(times, now, count=2):
    """
    Verilen saat listesinden şu andan itibaren sıradaki 'count' (varsayılan 2) seferi döndürür.
    Eğer o günkü tüm seferler bittiyse (gece yarısından sonra), ertesi günün ilk seferlerini gösterir.
    """
    if not times:
        return ["-", "-"]

    now_minutes = now.hour * 60 + now.minute
    minutes_list = [time_str_to_minutes(t) for t in times]

    start_index = None
    for i, m in enumerate(minutes_list):
        if m >= now_minutes:
            start_index = i
            break

    # Tüm seferler geçtiyse ertesi günün ilk seferine dön (indeks 0)
    if start_index is None:
        start_index = 0  

    result = []
    n = len(times)
    for i in range(count):
        # Liste sonuna gelindiğinde başa sarması için modulo (%) kullanıyoruz
        result.append(times[(start_index + i) % n])
    return result

def get_current_schedule(firma, direction_key):
    """
    Bugünün tarihine ve gün tipine (hafta içi, cmt, pzr) göre aktif tarifeyi seçer.
    """
    now = datetime.datetime.now()
    today_str = now.strftime('%Y-%m-%d')
    
    # Gün tipini belirle (0: Pzt, 6: Pzr)
    wd = now.weekday()
    if wd == 5: day_key = 'saturday'
    elif wd == 6: day_key = 'sunday'
    else: day_key = 'weekday'

    # İlgili firmanın tarih aralığına uyan tarifesini bul
    for tarife in VERI_HAVUZU.get(firma, []):
        if tarife['baslangic'] <= today_str <= tarife['bitis']:
            return tarife['seferler'].get(direction_key, {}).get(day_key, [])
            
    # Eğer tarih aralığına uyan aktif bir tarife yoksa, güvenlik için listedeki son tarifeyi döndür
    if VERI_HAVUZU.get(firma):
        return VERI_HAVUZU[firma][-1]['seferler'].get(direction_key, {}).get(day_key, [])
    return []

class VapurView(ui.View):
    def __init__(self):
        super().__init__()
        self.name = 'Kadıköy - Karaköy Vapur Saatleri'
        self.background_color = 'white'

        # Yön seçimi Segmented Control
        self.direction_control = ui.SegmentedControl()
        self.direction_control.segments = ['Kadıköy kalkış', 'Karaköy kalkış']
        self.direction_control.selected_index = 1  # varsayılan: Karaköy kalkış
        self.direction_control.action = self.direction_changed
        self.add_subview(self.direction_control)

        # Şu anki saati gösteren etiket
        self.time_label = ui.Label()
        self.time_label.alignment = ui.ALIGN_CENTER
        self.time_label.font = ('<System-Bold>', 18)
        self.add_subview(self.time_label)

        # Yenile butonu
        self.refresh_button = ui.Button(title='⟳')
        self.refresh_button.action = self.refresh_tapped
        self.refresh_button.font = ('<System>', 20)
        self.add_subview(self.refresh_button)

        # Firma Başlıkları
        self.sehir_title = ui.Label()
        self.sehir_title.text = 'Şehir Hatları'
        self.sehir_title.alignment = ui.ALIGN_CENTER
        self.sehir_title.font = ('<System-Bold>', 16)
        self.add_subview(self.sehir_title)

        self.turyol_title = ui.Label()
        self.turyol_title.text = 'Turyol'
        self.turyol_title.alignment = ui.ALIGN_CENTER
        self.turyol_title.font = ('<System-Bold>', 16)
        self.add_subview(self.turyol_title)

        # Şehir Hatları sıradaki 2 sefer etiketleri
        self.sehir_time1 = ui.Label()
        self.sehir_time2 = ui.Label()
        for lbl in (self.sehir_time1, self.sehir_time2):
            lbl.alignment = ui.ALIGN_CENTER
            lbl.font = ('<System>', 24)
            self.add_subview(lbl)

        # Turyol sıradaki 2 sefer etiketleri
        self.turyol_time1 = ui.Label()
        self.turyol_time2 = ui.Label()
        for lbl in (self.turyol_time1, self.turyol_time2):
            lbl.alignment = ui.ALIGN_CENTER
            lbl.font = ('<System>', 24)
            self.add_subview(lbl)

        # İlk açılışta verileri çek
        self.update_times()

    def layout(self):
        """Ekran boyutlarına göre arayüz elemanlarının yerleşimini (koordinatlarını) ayarlar."""
        w, h = self.width, self.height
        self.direction_control.frame = (10, 10, w - 60, 32)
        self.refresh_button.frame = (w - 40, 10, 30, 32)
        self.time_label.frame = (10, 50, w - 20, 30)
        
        col_w = (w - 30) / 2.0
        left_x = 10
        right_x = 20 + col_w
        
        self.sehir_title.frame = (left_x, 90, col_w, 24)
        self.turyol_title.frame = (right_x, 90, col_w, 24)
        
        self.sehir_time1.frame = (left_x, 120, col_w, 30)
        self.sehir_time2.frame = (left_x, 155, col_w, 30)
        self.turyol_time1.frame = (right_x, 120, col_w, 30)
        self.turyol_time2.frame = (right_x, 155, col_w, 30)

    def get_direction_key(self):
        """Kullanıcının seçtiği yönü veri havuzundaki anahtar kelimeye çevirir."""
        return 'kadikoy_karakoy' if self.direction_control.selected_index == 0 else 'karakoy_kadikoy'

    def direction_changed(self, sender):
        """Yön değiştirildiğinde saatleri günceller."""
        self.update_times()

    def refresh_tapped(self, sender):
        """Yenile butonuna basıldığında saatleri günceller."""
        self.update_times()

    def update_times(self):
        """Geçerli saate göre ekrandaki sefer verilerini yeniler."""
        now = datetime.datetime.now()
        self.time_label.text = now.strftime('Şu an: %H:%M')
        direction_key = self.get_direction_key()

        # Şehir Hatları Güncelleme
        sehir_list = get_current_schedule('sehir_hatlari', direction_key)
        s_next = get_next_departures(sehir_list, now, count=2)
        self.sehir_time1.text = s_next[0]
        self.sehir_time2.text = s_next[1]

        # Turyol Güncelleme
        turyol_list = get_current_schedule('turyol', direction_key)
        t_next = get_next_departures(turyol_list, now, count=2)
        self.turyol_time1.text = t_next[0]
        self.turyol_time2.text = t_next[1]

if __name__ == '__main__':
    v = VapurView()
    v.present('sheet')