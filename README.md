# ASTRA | Balistik ve Güdüm Simülasyonu

Bu proje, mühimmat uçuş dinamiklerinin modellenmesi ve güdüm algoritmalarının test edilmesi için geliştirilmiş bir teknik analiz platformudur.

## Teknik İçerik

- **Sayısal Metotlar:** 4. Derece Runge-Kutta (RK4) diferansiyel denklem çözücü.
- **Atmosferik Modelleme:** International Standard Atmosphere (ISA) verileri ile irtifaya bağlı yoğunluk hesaplaması.
- **Aerodinamik:** Mach sayısına ve sürtünme katsayısına (Cd) bağlı aerodinamik sürükleme kuvveti modellemesi.
- **Kontrol ve Güdüm:** Proportional Navigation (PN) kanunu kullanılarak rüzgar sapmalarının kompanse edilmesi.
- **Görselleştirme:** Plotly.js tabanlı 3D telemetri ve veri görselleştirme dashboard'u.

## Dosya Yapısı

- `include/Projectile.hpp`: Fizik motoru ve güdüm algoritması.
- `src/main.cpp`: Simülasyon döngüsü ve veri toplama.
- `index.html`: Senaryo analizi ve görselleştirme arayüzü.
- `simulate_and_visualize.py`: Sistem entegrasyon ve veri köprüsü.

## Çalıştırma

1. `index.html` dosyasını tarayıcıda açarak gerçek zamanlı simülasyonu başlatabilirsiniz.
2. C++ motorunu derleyerek yüksek hassasiyetli telemetri verileri üretebilirsiniz.

---
*Bireysel teknik araştırma ve geliştirme projesidir.*
