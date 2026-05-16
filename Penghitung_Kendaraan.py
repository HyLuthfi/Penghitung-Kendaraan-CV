import cv2
import numpy as np
import os

gunakan_kamera_langsung = False

jalur_video = os.path.join(os.path.dirname(__file__), 'traffic_video.mp4')
if gunakan_kamera_langsung:
    kamera_video = cv2.VideoCapture(0)
else:
    kamera_video = cv2.VideoCapture(jalur_video)

pemisah_latar = cv2.createBackgroundSubtractorMOG2(history=500, varThreshold=50, detectShadows=True)

garis_y = 250 
toleransi = 15

jumlah_motor = 0
jumlah_mobil = 0
jumlah_truk = 0

memori_titik_tengah = []
jumlah_frame = 0

while True:
    berhasil, frame = kamera_video.read()
    if not berhasil:
        break

    frame = cv2.resize(frame, (640, 480))
    jumlah_frame += 1

    abu_abu = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    masking_depan = pemisah_latar.apply(abu_abu)
    
    _, hasil_threshold = cv2.threshold(masking_depan, 200, 255, cv2.THRESH_BINARY)

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    morfologi = cv2.morphologyEx(hasil_threshold, cv2.MORPH_OPEN, kernel, iterations=1) 
    morfologi = cv2.morphologyEx(morfologi, cv2.MORPH_CLOSE, kernel, iterations=1)

    kumpulan_kontur, _ = cv2.findContours(morfologi, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    cv2.line(frame, (0, garis_y), (640, garis_y), (0, 255, 255), 2)
    cv2.putText(frame, "Garis Hitung", (10, garis_y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)

    for kontur in kumpulan_kontur:
        luas_area = cv2.contourArea(kontur)
        
        if luas_area < 500:
            continue
            
        x, y, lebar, tinggi = cv2.boundingRect(kontur)
        titik_tengah_x = x + int(lebar / 2)
        titik_tengah_y = y + int(tinggi / 2)
        luas_kotak = lebar * tinggi
        
        if luas_kotak < 3000:
            jenis = "Motor"
            warna = (0, 255, 0)
        elif 3000 <= luas_kotak < 60000:
            jenis = "Mobil"
            warna = (255, 0, 0)
        else:
            jenis = "Truk/Bus"
            warna = (0, 0, 255)
            
        cv2.rectangle(frame, (x, y), (x + lebar, y + tinggi), warna, 2)
        cv2.circle(frame, (titik_tengah_x, titik_tengah_y), 4, warna, -1)
        cv2.putText(frame, jenis, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, warna, 2)
        
        if (garis_y - toleransi) < titik_tengah_y < (garis_y + toleransi):
            sudah_dihitung = False
            for titik in memori_titik_tengah:
                if abs(titik_tengah_x - titik[0]) < 50 and abs(titik_tengah_y - titik[1]) < 50: 
                    if (jumlah_frame - titik[2]) < 30:
                        sudah_dihitung = True
                        break
            
            if not sudah_dihitung:
                memori_titik_tengah.append((titik_tengah_x, titik_tengah_y, jumlah_frame))
                
                if jenis == "Motor":
                    jumlah_motor += 1
                elif jenis == "Mobil":
                    jumlah_mobil += 1
                elif jenis == "Truk/Bus":
                    jumlah_truk += 1
                    
                cv2.line(frame, (0, garis_y), (640, garis_y), (0, 0, 255), 4)

    cv2.rectangle(frame, (10, 10), (250, 100), (0, 0, 0), -1)
    cv2.putText(frame, f"Motor   : {jumlah_motor}", (20, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
    cv2.putText(frame, f"Mobil   : {jumlah_mobil}", (20, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)
    cv2.putText(frame, f"Truk/Bus: {jumlah_truk}", (20, 85), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

    cv2.imshow("Video Asli (ATM Paper 2)", frame)
    cv2.imshow("Background Subtraction (Blob)", morfologi)

    if cv2.waitKey(30) & 0xFF == ord('q'):
        break

kamera_video.release()
cv2.destroyAllWindows()

print("\n HASIL AKHIR PENGHITUNGAN")
print(f"Total Motor   : {jumlah_motor}")
print(f"Total Mobil   : {jumlah_mobil}")
print(f"Total Truk/Bus: {jumlah_truk}")
print("Selesai.")
