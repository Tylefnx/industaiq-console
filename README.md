# ⚡ IndustAIQ Console

**Akıllı Endüstriyel Teşhis ve Bakım Sistemi**

IndustAIQ Console, endüstriyel makinelerden gelen alarm kodlarını gerçek zamanlı olarak analiz eden, AI destekli bir teşhis ve bakım yönetim sistemidir. ThingsBoard IoT platformu ile entegre çalışarak, makine telemetri verilerini alır ve yerel LLM (Ollama) kullanarak anında çözüm önerileri sunar.

---

## 🎯 Özellikler

- **AI Destekli Analiz**: Ollama ile yerel LLM kullanarak alarm kodlarını analiz eder ve çözüm önerileri sunar
- **Bilgi Tabanı**: PDF ve Excel formatındaki teknik dokümanlardan otomatik bilgi çıkarımı
- **Gerçek Zamanlı İzleme**: ThingsBoard WebSocket entegrasyonu ile canlı telemetri takibi
- **Çok Dilli Destek**: 10 dilde arayüz ve çeviri desteği
- **Akıllı Önbellekleme**: Daha önce analiz edilmiş alarmlar için anında yanıt
- **Otomatik Raporlama**: E-posta ile günlük bakım raporları

---

## 🏗️ Mimari

```
┌─────────────────┐
│  ThingsBoard    │
│  IoT Platform   │
└────────┬────────┘
         │ WebSocket/HTTP
         │ (Telemetry Data)
         ▼
┌─────────────────┐
│  IndustAIQ      │
│  Console        │
│                 │
│  ┌───────────┐  │
│  │ Streamlit │  │
│  │   UI      │  │
│  └─────┬─────┘  │
│        │        │
│  ┌─────▼─────┐  │
│  │ Monitor   │  │
│  │ Service   │  │
│  └─────┬─────┘  │
│        │        │
│  ┌─────▼─────┐  │
│  │Knowledge  │  │
│  │  Base     │  │
│  └─────┬─────┘  │
│        │        │
│  ┌─────▼─────┐  │
│  │ AI Engine │  │
│  │ (Ollama)  │  │
│  └───────────┘  │
└─────────────────┘
```

### Veri Akışı

1. **Telemetri Alımı**: ThingsBoard'dan WebSocket ile gerçek zamanlı veri
2. **Alarm Tespiti**: Gelen payload'lardan alarm kodları çıkarılır
3. **Bilgi Arama**: Knowledge Base'de ilgili dokümanlar aranır (PDF/Excel)
4. **AI Analizi**: Ollama LLM ile alarm analizi ve çözüm önerisi
5. **Önbellekleme**: Çözüm veritabanına kaydedilir
6. **UI Güncelleme**: Streamlit arayüzünde sonuçlar gösterilir

### Teknoloji Stack

- **Frontend**: Streamlit
- **Backend**: Python 3.8+
- **AI/ML**: Ollama (Local LLM), scikit-learn (TF-IDF)
- **IoT**: ThingsBoard, WebSocket Client
- **Veritabanı**: SQLite
- **PDF/Excel**: pypdf, pandas, openpyxl

---

## 🚀 Hızlı Başlangıç

### Gereksinimler

- Python 3.8+
- Ollama (yerel LLM servisi)
- ThingsBoard (IoT platform)

### Kurulum

```bash
# Depoyu klonla
git clone https://github.com/yourusername/endustry4.0.git
cd endustry4.0

# Sanal ortam oluştur
python -m venv venv
source venv/bin/activate  # Linux/Mac

# Bağımlılıkları yükle
pip install -r requirements.txt

# Ollama modelini indir
ollama pull llama3.1

# Ortam değişkenlerini yapılandır
cp .env.example .env
# .env dosyasını düzenle

# PDF dosyalarını sources/ klasörüne kopyala
mkdir -p sources
cp /path/to/manuals/*.pdf sources/

# Uygulamayı başlat
streamlit run main.py
```

### Yapılandırma (.env)

```env
# ThingsBoard
TB_BASE_URL=https://your-thingsboard-instance.com
TB_USER=tenant@thingsboard.org
TB_PASS=your_password
TB_DEVICE_ID=your_device_id

# Ollama
LLM_BASE_URL=http://localhost:11434/v1
AI_MODEL_ID=llama3.1

# Dizinler
PDF_SOURCE_DIR=sources
CACHE_DIR=cache
```

---

## 📁 Proje Yapısı

```
endustry4.0/
├── main.py                 # Ana giriş noktası
├── src/
│   ├── core/              # AI Engine, Knowledge Base, Telemetry
│   ├── services/          # Monitor, Database, Logger, Reporter
│   ├── ui/                # Streamlit UI bileşenleri
│   └── scripts/           # Cache warmer gibi yardımcı scriptler
├── sources/               # PDF ve Excel kaynak dosyaları
├── cache/                 # PDF işleme cache'i
└── tests/                 # Test dosyaları
```

---

## 🔮 Gelecek Vizyonu

Proje, **akıllı ve otonom bakım** özelliklerine doğru gelişmektedir:

- **Tahminsel Bakım**: Geçmiş alarm verilerini analiz ederek olası arızaları önceden tespit etme
- **Otonom Karar Verme**: Makine öğrenmesi modelleri ile otomatik bakım önerileri
- **Veri Analitiği**: Tarihsel verilerden pattern çıkarma ve trend analizi
- **Bakım Optimizasyonu**: Bakım zamanlaması ve kaynak optimizasyonu

---

## 📝 Lisans

Bu proje [GNU General Public License v2.0](LICENSE) altında lisanslanmıştır.

---

## 🤝 Katkıda Bulunma

Katkılarınızı bekliyoruz! Pull request'ler memnuniyetle karşılanır.

---

**Versiyon**: 2.0
