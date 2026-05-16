# Penghitung Kendaraan Otomatis (Tugas 1)

Repositori ini berisi implementasi **Tugas 1 - Computer Vision**, yaitu sistem pendeteksi, pengklasifikasi, dan penghitung kendaraan otomatis pada video jalan raya menggunakan algoritma **Background Subtraction MOG2** dan **Blob Detection** dari OpenCV.

Sistem ini dirancang menggunakan pendekatan *Amati, Tiru, Modifikasi (ATM)* berdasarkan literatur riset pengolahan citra digital untuk memonitor kepadatan lalu lintas.

## Fitur Utama
- **Deteksi Objek Dinamis**: Memanfaatkan `cv2.createBackgroundSubtractorMOG2` (termasuk deteksi bayangan) untuk memisahkan objek yang bergerak (kendaraan) dari latar belakang yang statis (jalan raya).
- **Klasifikasi Berbasis Area (*Bounding Box*)**: Mengkategorikan kendaraan berdasarkan estimasi ukuran luas (*width* × *height*):
  - 🟢 **Motor**: Luas `< 3000` piksel
  - 🔵 **Mobil**: Luas `3000 - 60000` piksel
  - 🔴 **Truk/Bus**: Luas `> 60000` piksel
- **Garis Hitung Virtual (*Region of Interest*)**: Kendaraan hanya dihitung ketika titik tengahnya (*centroid*) menyentuh area garis maya dengan nilai toleransi. Dilengkapi algoritma rekam jejak memori untuk **mencegah penghitungan ganda** (*double-count prevention*) pada objek yang sama.

## Prasyarat (Dependencies)
Pastikan Anda telah menginstal modul Python berikut di dalam *environment* Anda:
```bash
pip install opencv-python numpy
```

## Cara Menjalankan
1. *Clone* repositori ini ke komputer Anda.
2. Pastikan file sampel video lalu lintas (`traffic_video.mp4`) berada di direktori yang sama dengan kode *script*.
3. Buka terminal dan jalankan *script* utama:
```bash
python Penghitung_Kendaraan.py
```
4. Sebuah jendela *preview* proses Computer Vision akan terbuka. Tekan tombol **`q`** pada keyboard untuk menghentikan pemutaran secara manual.

## Struktur Repositori
- `Penghitung_Kendaraan.py` — File kode utama (*pipeline* Computer Vision).
- `traffic_video.mp4` — (Opsional) File video masukan (*input*).

## Contoh *Output* Log Terminal
Ketika video telah selesai diputar atau dihentikan, terminal akan mencetak laporan komprehensif:
```text
 HASIL AKHIR PENGHITUNGAN
Total Motor   : 0
Total Mobil   : 4
Total Truk/Bus: 0
Selesai.
```
