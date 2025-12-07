import cv2                # Library OpenCV: Untuk "mata" komputer (buka kamera, olah gambar)
import mediapipe as mp    # Library MediaPipe: "Otak" AI buatan Google untuk deteksi tangan

# ==========================================
# BAGIAN 1: PERSIAPAN (SETUP)
# ==========================================

# Menyiapkan modul deteksi tangan
mp_hands = mp.solutions.hands           
mp_drawing = mp.solutions.drawing_utils # Modul untuk menggambar garis tulang tangan di layar

# Membuka kamera laptop (angka 0 biasanya untuk webcam internal)
cap = cv2.VideoCapture(0)

# List ID ujung jari (berdasarkan diagram MediaPipe):
# 4=Jempol, 8=Telunjuk, 12=Tengah, 16=Manis, 20=Kelingking
id_ujung_jari = [4, 8, 12, 16, 20]

# Memulai AI Deteksi Tangan
# min_detection_confidence=0.5 artinya AI harus yakin minimal 50% bahwa itu tangan
with mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands:
    
    print("Program Berjalan! Tekan 'q' untuk keluar.")

    # Loop utama: Program akan terus berulang selama kamera terbuka
    while cap.isOpened():            
        
        # --- A. BACA GAMBAR ---
        sukses, gambar = cap.read() # Membaca satu frame gambar dari kamera
        if not sukses:              # Jika kamera error atau tertutup
            continue

        # --- B. PRA-PEMROSESAN GAMBAR ---
        # Membalik gambar (Mirroring) agar gerakan tangan natural seperti bercermin
        # Parameter '1' artinya flip secara horizontal
        gambar = cv2.flip(gambar, 1)
        
        # Mengubah warna dari BGR (format OpenCV) ke RGB (format yang dimengerti MediaPipe)
        gambar_rgb = cv2.cvtColor(gambar, cv2.COLOR_BGR2RGB)
        
        # AI memproses gambar untuk mencari tangan
        hasil = hands.process(gambar_rgb)

        # --- C. LOGIKA UTAMA (JIKA TANGAN DITEMUKAN) ---
        if hasil.multi_hand_landmarks:
            
            # Loop untuk menangani setiap tangan yang muncul (bisa kiri, kanan, atau keduanya)
            # 'enumerate' dipakai untuk mendapatkan index (idx) urutan tangan
            for idx, tangan_landmarks in enumerate(hasil.multi_hand_landmarks):
                
                # Mendapatkan Label: Apakah ini tangan "Left" (Kiri) atau "Right" (Kanan)?
                label_tangan = hasil.multi_handedness[idx].classification[0].label

                # 1. Menggambar tulang tangan di layar (Visualisasi)
                mp_drawing.draw_landmarks(
                    gambar, tangan_landmarks, mp_hands.HAND_CONNECTIONS)
                
                # 2. Menyimpan posisi jari ke dalam List agar bisa dihitung
                list_titik = []
                tinggi, lebar, c = gambar.shape # Mengambil ukuran layar kamera
                
                # Mengubah koordinat desimal (0.5) menjadi pixel (misal: x=300, y=400)
                for id, lm in enumerate(tangan_landmarks.landmark):
                    cx, cy = int(lm.x * lebar), int(lm.y * tinggi)
                    list_titik.append({'id': id, 'x': cx, 'y': cy})

                # 3. LOGIKA MENGHITUNG JARI TERBUKA
                jari_terbuka = [] 

                # --- CEK JEMPOL (Spesial: Bergerak ke Samping/Sumbu X) ---
                # Jempol punya logika beda untuk tangan Kanan vs Kiri
                
                if label_tangan == "Right":
                    # Tangan Kanan: Jempol terbuka jika Ujung (4) ada di sebelah KIRI Sendi (3)
                    # Di layar komputer, "Kiri" artinya nilai X lebih kecil
                    if list_titik[4]['x'] < list_titik[3]['x']:
                        jari_terbuka.append(1) # 1 artinya terbuka
                    else:
                        jari_terbuka.append(0) # 0 artinya tertutup
                else:
                    # Tangan Kiri: Jempol terbuka jika Ujung (4) ada di sebelah KANAN Sendi (3)
                    if list_titik[4]['x'] > list_titik[3]['x']:
                        jari_terbuka.append(1)
                    else:
                        jari_terbuka.append(0)

                # --- CEK 4 JARI LAINNYA (Bergerak ke Atas/Sumbu Y) ---
                # Kita cek Telunjuk(8), Tengah(12), Manis(16), Kelingking(20)
                for id in [8, 12, 16, 20]:
                    # Di komputer, koordinat Y=0 ada di ATAS layar. 
                    # Jadi jika Y Ujung Jari LEBIH KECIL dari Y Sendi bawahnya (id-2),
                    # Berarti jari itu sedang NAIK (Terbuka).
                    if list_titik[id]['y'] < list_titik[id - 2]['y']:
                        jari_terbuka.append(1) 
                    else:
                        jari_terbuka.append(0) 

                # Hitung total jari yang nilainya 1 (terbuka)
                jumlah_jari = jari_terbuka.count(1)

                # --- D. MENENTUKAN NAMA GESTUR ---
                teks_gestur = ""
                if jumlah_jari == 0:
                    teks_gestur = "MENGEPAL"
                elif jumlah_jari == 1:
                    teks_gestur = "SATU"
                elif jumlah_jari == 2:
                    # Cek khusus: Jika jari Telunjuk dan Tengah yang terbuka = Peace
                    if jari_terbuka[1] == 1 and jari_terbuka[2] == 1:
                        teks_gestur = "PEACE"
                    else:
                        teks_gestur = "DUA"
                elif jumlah_jari == 3:
                    teks_gestur = "TIGA"
                elif jumlah_jari == 4:
                    teks_gestur = "EMPAT"
                elif jumlah_jari == 5:
                    teks_gestur = "HAI / STOP / LIMA"
                
                # --- E. MENAMPILKAN TEKS DI LAYAR ---
                # Mengatur posisi teks agar tidak bertumpuk jika ada 2 tangan
                posisi_x = 10 
                if label_tangan == "Right":
                    posisi_y_judul = 50   # Tangan kanan teksnya di atas
                    posisi_y_teks = 80
                    warna_teks = (0, 255, 0) # Warna Hijau (BGR)
                else:
                    posisi_y_judul = 150  # Tangan kiri teksnya di bawah
                    posisi_y_teks = 180
                    warna_teks = (255, 0, 255) # Warna Ungu

                # Menulis Label Tangan & Jumlah Jari
                cv2.putText(gambar, f"{label_tangan}: {jumlah_jari}", (posisi_x, posisi_y_judul), 
                            cv2.FONT_HERSHEY_PLAIN, 2, warna_teks, 2)
                
                # Menulis Nama Gestur (jika ada)
                if teks_gestur:
                    cv2.putText(gambar, teks_gestur, (posisi_x, posisi_y_teks), 
                                cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 0), 2)

        # --- F. RENDER LAYAR ---
        cv2.imshow('Kamera Deteksi Tangan', gambar)

        # Cek tombol keyboard. Jika 'q' atau ESC ditekan, loop berhenti.
        tombol = cv2.waitKey(1)
        if tombol == 27 or tombol == ord('q'):
            break

# Membersihkan kamera dan menutup jendela
cap.release()
cv2.destroyAllWindows()