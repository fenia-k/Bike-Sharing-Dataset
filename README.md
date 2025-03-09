# Bike Sharing Dashboard

Dashboard interaktif untuk menganalisis pola penggunaan layanan bike sharing berdasarkan faktor musim, cuaca, dan jenis pengguna.

## Deskripsi Proyek

Proyek ini menganalisis dataset Bike Sharing untuk mengidentifikasi pola peminjaman sepeda dan perbedaan perilaku antara pengguna casual dan registered. Tujuan utama adalah menjawab pertanyaan bisnis berikut:
1. Bagaimana pola peminjaman sepeda berubah berdasarkan musim dan kondisi cuaca?
2. Bagaimana perbedaan perilaku antara pengguna biasa (casual) dan pengguna terdaftar (registered) dalam peminjaman sepeda?

Analisis yang dilakukan meliputi:
- Pengaruh musim dan kondisi cuaca terhadap jumlah peminjaman sepeda
- Perbandingan perilaku peminjaman antara pengguna biasa (casual) dan pengguna terdaftar (registered)
- Trend penggunaan sepeda berdasarkan bulan, musim, dan kondisi cuaca
- Analisis segmentasi pengguna menggunakan model RFM (Recency, Frequency, Monetary)

## Struktur Proyek

```
submission/
├── dashboard/
│   ├── dashboard.py          # Aplikasi Streamlit
│   └── requirements.txt      # Library untuk dashboard
├── data/
│   ├── day.csv               # Dataset harian
│   └── hour.csv              # Dataset per jam
├── notebook.ipynb            # Notebook analisis data
├── README.md                 # Dokumentasi proyek
└── requirements.txt          # Daftar library untuk proyek
└── url.txt
```

## Setup Environment

Untuk menjalankan dashboard, Anda perlu menginstal library yang diperlukan. Jalankan perintah berikut di terminal:

```bash
pip install -r requirements.txt
```

Library utama yang digunakan dalam proyek ini:
- streamlit==1.27.0
- pandas==2.1.0
- numpy==1.24.3
- matplotlib==3.7.2
- seaborn==0.12.2

## Menjalankan Dashboard

Untuk menjalankan dashboard, gunakan perintah berikut:

```bash
cd dashboard
streamlit run dashboard.py
```

Dashboard akan terbuka di browser web default Anda. Jika tidak terbuka secara otomatis, Anda dapat mengakses dashboard di http://localhost:8501.

## Fitur Dashboard

Dashboard ini menyediakan beberapa fitur:

1. **Filter Data**
   - Filter berdasarkan rentang tanggal
   - Filter berdasarkan musim (Spring, Summer, Fall, Winter)
   - Filter berdasarkan kondisi cuaca (Clear, Misty, Light Rain/Snow, Heavy Rain/Snow)
   
2. **Analisis Musim dan Cuaca**
   - Visualisasi rata-rata peminjaman sepeda per musim
   - Visualisasi rata-rata peminjaman sepeda berdasarkan kondisi cuaca
   - Interaksi musim dan kondisi cuaca terhadap peminjaman sepeda
   - Tren peminjaman sepeda bulanan berdasarkan musim dan cuaca
   - Pola peminjaman sepeda berdasarkan jam dan hari
   
3. **Analisis Pengguna**
   - Perbandingan total peminjaman antara pengguna casual dan registered
   - Perbandingan peminjaman berdasarkan musim dan tipe pengguna
   - Pola peminjaman berdasarkan hari dalam seminggu untuk setiap tipe pengguna
   - Pola peminjaman berdasarkan jam dan tipe pengguna
   - Peminjaman berdasarkan tipe hari (kerja vs libur) dan tipe pengguna
   - Pengaruh kondisi cuaca terhadap tipe pengguna
   
4. **Kesimpulan dan Rekomendasi**
   - Ringkasan insight utama dari analisis
   - Rekomendasi bisnis berdasarkan temuan untuk strategi marketing, manajemen operasional, dan pengembangan produk

## Detail Dataset

Dataset Bike Sharing terdiri dari dua file:
1. **day.csv**: Data agregat harian dengan 731 entri
2. **hour.csv**: Data per jam dengan 17,379 entri

Variabel-variabel dalam dataset:
- **instant**: ID record
- **dteday**: Tanggal
- **season**: Musim (1: Spring, 2: Summer, 3: Fall, 4: Winter)
- **yr**: Tahun (0: 2011, 1: 2012)
- **mnth**: Bulan (1-12)
- **hr**: Jam (0-23)
- **holiday**: Flag hari libur
- **weekday**: Hari dalam seminggu
- **workingday**: Flag hari kerja
- **weathersit**: Kondisi cuaca
  - 1: Clear/Few clouds
  - 2: Mist/Cloudy
  - 3: Light Snow/Rain
  - 4: Heavy Rain/Snow/Fog
- **temp**: Suhu dalam Celsius (normalisasi)
- **atemp**: Suhu terasa dalam Celsius (normalisasi)
- **hum**: Kelembaban (normalisasi)
- **windspeed**: Kecepatan angin (normalisasi)
- **casual**: Jumlah pengguna casual
- **registered**: Jumlah pengguna registered
- **cnt**: Total jumlah peminjaman sepeda

## Proses Analisis Data

Proses analisis data yang dilakukan dalam proyek ini mencakup:

1. **Data Wrangling**
   - Gathering data dari sumber (dataset Bike Sharing)
   - Assessing data untuk mendeteksi masalah kualitas (duplicates, missing values, inconsistent data)
   - Cleaning data: menangani missing values, duplikasi, dan outlier
   - Mengubah tipe data (seperti mengkonversi dteday ke format datetime)
   - Memastikan konsistensi nilai pada kolom kategorikal (season, weathersit, weekday)

2. **Exploratory Data Analysis (EDA)**
   - Analisis statistik deskriptif untuk memahami distribusi data
   - Analisis korelasi untuk mengidentifikasi hubungan antar variabel
   - Eksplorasi pola peminjaman berdasarkan musim, cuaca, waktu, dan jenis pengguna

3. **Visualisasi dan Interpretasi**
   - Pembuatan berbagai visualisasi untuk mengidentifikasi pola dan tren
   - Interpretasi hasil dan penarikan insight bisnis
   - Pengembangan rekomendasi berdasarkan temuan

## Kesimpulan Utama

Dari analisis yang dilakukan, diperoleh kesimpulan utama:

1. **Pertanyaan 1: Pola Peminjaman Sepeda Berdasarkan Musim dan Kondisi Cuaca**

   Peminjaman sepeda mencapai puncak pada musim gugur (211.53) dan musim panas (189.46), dengan penurunan signifikan pada musim semi (108.41) dan musim dingin (180.87). Cuaca cerah konsisten menghasilkan peminjaman tertinggi (185.31), sementara cuaca mendung (162.06) dan hujan (106.05) mengurangi jumlah peminjaman secara bertahap. Bulan Mei-September menunjukkan aktivitas tertinggi, sedangkan Januari-Februari terendah. Faktor cuaca memiliki dampak lebih besar pada musim dingin, dengan penurunan ekstrem saat hujan.

2. **Pertanyaan 2: Perbedaan Perilaku Pengguna Casual dan Registered**

   Pengguna registered mendominasi total peminjaman dengan pola penggunaan yang lebih konsisten sepanjang tahun dan lebih stabil pada hari kerja, menunjukkan penggunaan untuk komuter rutin. Pengguna casual menunjukkan fluktuasi lebih ekstrem berdasarkan musim, meningkat pada akhir pekan dan menurun drastis saat musim dingin atau cuaca buruk, mengindikasikan penggunaan rekreasional. Pola harian registered menunjukkan dua puncak (pagi dan sore) yang mencerminkan pola komuter, sementara casual memiliki puncak tunggal di siang hingga sore hari.

## Rekomendasi Bisnis

Berdasarkan analisis, berikut adalah rekomendasi bisnis:

1. **Strategi Marketing**:
   - Meningkatkan promosi untuk mengkonversi pengguna casual menjadi registered dengan penawaran khusus pada akhir musim semi
   - Membuat "Weekend Pass" dengan insentif khusus untuk pengguna casual yang sering bersepeda pada akhir pekan
   - Program loyalitas musiman dengan diskon untuk pengguna registered selama musim dingin dan cuaca buruk

2. **Manajemen Operasional**:
   - Distribusi sepeda berbasis lokasi dan waktu - fokus pada area perkantoran pagi/sore hari dan area rekreasi siang/akhir pekan
   - Mengurangi armada beroperasi saat cuaca buruk dan mengalokasikan untuk pemeliharaan
   - Meningkatkan ketersediaan sepeda di area transit pada jam puncak pengguna registered (7-9 pagi, 17-19 sore)

3. **Pengembangan Produk**:
   - Penambahan fitur perlindungan cuaca sederhana pada sepeda untuk meminimalkan dampak cuaca mendung/hujan ringan
   - Pengembangan paket langganan fleksibel untuk casual users dengan opsi penggunaan akhir pekan
   - Implementasi teknologi untuk memudahkan transisi dari pengguna casual ke registered, seperti upgrade membership langsung dari aplikasi

## Sumber Data

Dataset yang digunakan dalam proyek ini adalah Bike Sharing Dataset, tersedia di [Kaggle](https://www.kaggle.com/datasets/lakshmi25npathi/bike-sharing-dataset).

## Penulis

Fenia Karenina br Surbakti  
Email: mc185d5x0359@student.devacademy.id  
ID Dicoding: MC185D5X0359

---

© 2025 Bike Sharing Analysis Project  
Proyek ini dikembangkan sebagai bagian dari submission Dicoding "Belajar Analisis Data dengan Python".