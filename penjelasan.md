# Penjelasan Workflow Aplikasi Prediksi (Stunting & Mata Minus)

Dokumen ini menjelaskan alur kerja aplikasi dari awal sampai akhir agar mudah dijelaskan pada ujian lisan.

---

## 1) Tujuan Aplikasi
Aplikasi berbasis **Flask (Python)** ini memiliki 2 menu prediksi:
1. **Prediksi Stunting (Balita)** dengan model **KNN**.
2. **Prediksi Mata Minus / Kesehatan Mata** dengan model **KNN**.

Hasil prediksi ditampilkan langsung pada halaman web sehingga pengguna bisa mengisi data dan melihat output.

---

## 2) Struktur Project
Folder project terbagi menjadi beberapa komponen utama:
- **`app.py`**: backend Flask (memuat model, mengatur route, memproses input).
- **`templates/index.html`**: frontend (UI form dan hasil prediksi).
- **`static/style.css`**: styling tampilan (layout elegan 2 kolom).
- **Folder model**:
  - `Stunting/` berisi `model_knn_stunting.pkl` dan `scaler.pkl`.
  - `mata minus/` berisi `model_knn_eye_health.pkl` dan `scaler_eye_health.pkl`.

Model disimpan dalam format `.pkl` agar bisa langsung dimuat saat server berjalan.

---

## 3) Backend Flask: Alur Kerja di `app.py`

### 3.1 Memuat model dan scaler (startup)
Saat aplikasi dijalankan, `app.py`:
1. Memuat model stunting:
   - `Stunting/model_knn_stunting.pkl`
   - `Stunting/scaler.pkl`
2. Memuat model mata minus:
   - `mata minus/model_knn_eye_health.pkl`
   - `mata minus/scaler_eye_health.pkl`

Jika file tidak ditemukan atau gagal dimuat, variabel model/scaler akan bernilai `None` dan route akan mengembalikan error yang sesuai.

---

## 4) Route Prediksi (API Endpoint)

Aplikasi membuat **route terpisah** supaya stunting dan mata minus tidak bercampur.

### 4.1 Route Stunting
- Endpoint: **`POST /predict_stunting`**
- Input dari form:
  - `umur`
  - `jenis_kelamin` (laki-laki / perempuan)
  - `tinggi`

Langkah prosesnya:
1. Ambil input dari `request.form`.
2. Validasi:
   - Umur dan tinggi harus bisa diubah ke float.
   - Umur tidak boleh negatif.
   - Jenis kelamin harus salah satu dari `laki-laki` atau `perempuan`.
3. Konversi jenis kelamin ke fitur numerik (one-hot sederhana):
   - `jk = 1` untuk laki-laki
   - `jk = 0` untuk perempuan
4. Bentuk array fitur sesuai training:
   - `[umur, jk, tinggi]`
5. Normalisasi menggunakan scaler:
   - `features_scaled = stunting_scaler.transform(features)`
6. Prediksi dengan KNN:
   - `prediction = stunting_model.predict(features_scaled)[0]`
7. Konversi output kelas ke label manusiawi menggunakan mapping:
   - 0..3 → (Normal / Sangat Pendek / Pendek / Tinggi)
8. Kirim hasil ke `index.html` melalui variabel:
   - `prediction_text_stunting`

---

### 4.2 Route Mata Minus (Eye Health)
- Endpoint: **`POST /predict_eye`**
- Input dari form mata minus (sesuai fitur model):
  - `exercise_hours`
  - `mental_health_score`
  - `screen_time_hours`
  - `screen_brightness_avg`
  - `age`
  - `height_cm`
  - `outdoor_light_exposure_hours`
  - `night_mode_usage`
  - `screen_distance_cm`
  - `glasses_number`

Langkah prosesnya:
1. Memastikan model dan scaler mata minus tersedia.
2. Mengambil seluruh input satu per satu dari `request.form`.
3. Validasi bahwa setiap input **wajib diisi**.
4. Membentuk vektor fitur sesuai urutan training (penting agar fitur benar):
   - [exercise_hours, mental_health_score, ..., glasses_number]
5. Normalisasi dengan scaler:
   - `features_scaled = eye_scaler.transform(features)`
6. Prediksi dengan KNN:
   - `prediction = eye_model.predict(features_scaled)[0]`
7. Mapping hasil kelas menjadi label manusiawi:
   - 0..3 → (Rendah / Sedang / Tinggi / Sangat Tinggi)
8. Kirim hasil ke `index.html` melalui variabel:
   - `prediction_text_eye`

---

## 5) Frontend: `templates/index.html`
Frontend dirancang untuk presentasi:
- Halaman memiliki **2 card** dalam layout **grid 2 kolom**:
  - Card kiri: **Form Stunting** + output `prediction_text_stunting`.
  - Card kanan: **Form Mata Minus** + output `prediction_text_eye`.

Tombol:
- “Prediksi Sekarang” untuk masing-masing model.
- Tombol “Hapus Input” menggunakan JavaScript untuk mengosongkan form masing-masing card.

---

## 6) Styling: `static/style.css`
CSS membuat tampilan lebih elegan dan rapi:
- Background gambar dan efek blur di card.
- Grid responsif: jika layar kecil, kolom berubah menjadi 1 kolom.
- Warna tombol dan komponen seragam.

Tujuannya agar saat ujian lisan, tampilan terlihat profesional dan mudah digunakan.

---

## 7) Workflow Lengkap dari Awal hingga Akhir
Urutan yang terjadi saat pengguna memakai aplikasi:

1. **User membuka browser** dan mengakses endpoint `/`.
2. `app.py` mengembalikan `index.html` dengan form kosong.
3. User mengisi data:
   - Jika ingin stunting: isi `umur`, `jenis_kelamin`, `tinggi`.
   - Jika ingin mata minus: isi 10 fitur kesehatan mata.
4. User menekan tombol “Prediksi Sekarang”.
5. Browser mengirim request POST ke endpoint masing-masing:
   - `/predict_stunting` atau `/predict_eye`.
6. Backend:
   - Validasi input
   - Scaling menggunakan scaler
   - Prediksi menggunakan model KNN
   - Mapping kelas menjadi label
7. Backend mengembalikan kembali halaman `index.html` dengan output prediksi.
8. User melihat hasil pada card yang sesuai.

---

## 8) Keunggulan Implementasi (untuk diucapkan saat ujian)
- **Model terpisah** dan route terpisah → lebih jelas dan rapi.
- **Scaling sebelum prediksi** → sesuai praktik machine learning.
- **Tampilan presentatif** dengan 2 card → memudahkan demo ke guru.
- Ada **validasi input** supaya hasil tidak error saat user lupa mengisi.

---

Jika dibutuhkan, kamu bisa menambahkan contoh input dummy saat presentasi agar guru bisa melihat alur prediksi berjalan.
