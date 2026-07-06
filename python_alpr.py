import cv2
import imutils
import numpy as np
import easyocr


def process_image_for_alpr(image_path):
    """
    ALPR için görüntüyü okur, klasik görüntü işleme adımlarını uygular
    ve plakayı tespit edip OCR ile metne dönüştürür.
    """
    # 1. Görüntüyü Oku
    img = cv2.imread(image_path)
    if img is None:
        print("Hata: Görüntü bulunamadı. Lütfen dosya yolunu kontrol edin.")
        return

    # 2. Gri Tonlamaya Çevir (Grayscale Conversion)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 3. Gürültüyü Azalt (Gaussian Blurring / Bilateral Filter)
    # Bilateral filter kenarları korurken gürültüyü silmek için idealdir.
    bfilter = cv2.bilateralFilter(gray, 11, 17, 17)

    # 4. Kenar Tespiti (Canny Edge Detection)
    edged = cv2.Canny(bfilter, 30, 200)

    # 5. Kontur Tespiti (Contour Detection)
    keypoints = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(keypoints)
    # Konturları boyutlarına göre sırala ve en büyük 10 tanesini al
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]

    location = None

    # Plaka olabilecek dikdörtgen şekli bul
    for contour in contours:
        approx = cv2.approxPolyDP(contour, 10, True)
        if len(approx) == 4:  # 4 köşe = Dikdörtgen
            location = approx
            break

    if location is None:
        print("Plaka konturu bulunamadı.")
        return

    # 6. Sadece Plaka Kısmını Kırp (Cropping)
    mask = np.zeros(gray.shape, np.uint8)
    new_image = cv2.drawContours(mask, [location], 0, 255, -1)
    new_image = cv2.bitwise_and(img, img, mask=mask)

    (x, y) = np.where(mask == 255)
    (x1, y1) = (np.min(x), np.min(y))
    (x2, y2) = (np.max(x), np.max(y))
    cropped_image = gray[x1:x2 + 1, y1:y2 + 1]

    # 7. OCR İşlemi (EasyOCR ile metin çıkarma)
    print("OCR motoru çalıştırılıyor, lütfen bekleyin...")
    reader = easyocr.Reader(['en'])
    result = reader.readtext(cropped_image)

    # Sonucu Terminale Yazdır
    if result:
        text = result[0][-2]
        print("=" * 30)
        print(f"TESPİT EDİLEN PLAKA: {text}")
        print("=" * 30)
    else:
        print("Plaka kırpıldı ancak metin okunamadı.")


# Kodu çalıştırmak için dosya yolunu buraya girin
if __name__ == "__main__":
    # Kendi araba görselinin adını buraya yazmalısın
    TARGET_IMAGE = "car_plate.jpg"
    process_image_for_alpr(TARGET_IMAGE)