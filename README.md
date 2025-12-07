# ✋ Hand Gesture Recognition (MediaPipe + OpenCV)

![Python](https://img.shields.io/badge/Python-3.x-blue.svg)
![OpenCV](https://img.shields.io/badge/OpenCV-RealTime-green.svg)
![MediaPipe](https://img.shields.io/badge/MediaPipe-HandTracking-orange.svg)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux-lightgrey.svg)

Aplikasi **pendeteksi gerakan tangan secara real-time** menggunakan webcam.  
Menggunakan **MediaPipe** dan **OpenCV** untuk mendeteksi tangan dan menghitung jumlah jari.

---

## ✨ Fitur

- Deteksi tangan kanan & kiri
- Hitung jumlah jari otomatis
- Deteksi gestur (Mengepal, Angka, Peace, Stop)
- Tampilan real-time dari webcam

---

## 💡 Cara Kerja Singkat

Webcam membaca frame video

MediaPipe mendeteksi landmark (titik) pada tangan

Program menghitung jari yang terbuka

Gestur ditampilkan secara real-time di layar

---

## 🛠️ Instalasi

Pastikan Python sudah terinstall:

```bash
python --version

python -m pip install mediapipe opencv-python
```

---

## ▶️ Cara Menjalankan Program

Masuk ke folder project lalu jalankan:

```bash
python hand_gesture.py
```

Program akan:

Menyalakan kamera

Menampilkan jendela video

Menampilkan jumlah jari & nama gestur

🎮 Kontrol:

Tekan Q atau ESC untuk keluar

---

## 📌 Teknologi

Python

OpenCV

MediaPipe

---

## ⚠️ Catatan

Pastikan webcam tidak sedang dipakai aplikasi lain

Gunakan pencahayaan yang cukup agar deteksi lebih akurat

---

## 📜 Lisensi

Proyek ini dibuat untuk keperluan pembelajaran dan bebas digunakan.

---

## Anggota Kelompok 3

- Muhammad Rafif Nuha Daniswara / 5324600006
- Sulistyawati Adi Putri / 5324600008
- Arya Bagus Permono / 5324600017
- Andy Fajri Danio / 5324600027
- ⁠Ariq Rifky Ghiffari / 5324600028
