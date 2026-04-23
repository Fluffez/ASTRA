# ASTRA | İleri Seviye Balistik ve Güdüm Simülasyon Platformu

Bu proje, yüksek hassasiyetli mühimmatların uçuş dinamiklerini modellemek, yörünge analizi yapmak ve aktif güdüm algoritmalarını test etmek amacıyla geliştirilmiş bir mühendislik platformudur. Sistem, çekirdek fizik motoru olarak C++ tabanlı bir mimari kullanırken, analiz ve görselleştirme katmanında modern web teknolojileriyle entegre çalışır.

## Teknik Özellikler

- **Sayısal Çözümleyici:** 4. Derece Runge-Kutta (RK4) entegrasyon yöntemi ile yüksek hassasiyetli diferansiyel denklem çözümü.
- **Atmosfer Modeli:** International Standard Atmosphere (ISA) modeli entegrasyonu (Troposferik irtifaya bağlı değişken hava yoğunluğu ve sıcaklık hesaplamaları).
- **Aerodinamik Katsayılar:** Mach sayısına bağlı değişken sürükleme katsayısı (Transonik/Süpersonik Drag Spike) modellemesi.
- **Aktif Güdüm:** Proportional Navigation (PN) güdüm kanunu ile rüzgar ve dış etkenlere karşı gerçek zamanlı rota düzeltme (Closed-loop control).
- **Gerçek Zamanlı Analiz:** Javascript (Plotly.js) tabanlı 3D telemetri görselleştirme ve mühendislik dashboard'u.

## Proje Yapısı

- `include/Projectile.hpp`: Fizik motoru ve güdüm algoritmalarının matematiksel implementasyonu.
- `src/main.cpp`: Simülasyon döngüsü ve telemetri veri toplama katmanı.
- `index.html`: Çoklu senaryo analizi ve 3D yörünge karşılaştırma arayüzü.
- `simulate_and_visualize.py`: C++ çıktılarını dashboard katmanına aktaran veri köprüsü.

## Kullanım

Sistem iki şekilde çalıştırılabilir:
1. **Dinamik Mod:** `index.html` üzerinden parametreleri (açı, hedef, rüzgar) girerek tarayıcı içindeki fizik motoruyla anlık hesaplama.
2. **Yüksek Hassasiyetli Mod:** C++ motorunu derleyip çalıştırarak elde edilen telemetri verilerinin Python üzerinden dashboard'a aktarılması.

---
*Bu çalışma, balistik sistemler ve uçuş kontrol algoritmaları üzerine yürütülen bireysel bir Ar-Ge projesidir.*
