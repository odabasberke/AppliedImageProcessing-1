## 📌 Proje Özeti
Derin öğrenme modelleri genellikle birer "kara kutu" olarak çalışır. Bu proje, verileri bir yapay zeka metin motoruna teslim etmeden önce, hesaplama gürültüsünü (noise) radikal bir şekilde azaltmak için klasik matematiksel filtrelerin ve geometrik algoritmaların gücünü göstermektedir.

Sistem mimarisi, yapılandırılmış 4 adımlı bir görüntü işleme hattını (pipeline) ve ardından gelen karakter çıkarımını takip eder.

## 🛠️ Görüntü İşleme Hattı (Pipeline)
1. **Gri Tonlamaya Dönüştürme (Grayscale Conversion):** Görüntüyü tek bir yoğunluk kanalına indirgeyerek renk bağımlılıklarını ortadan kaldırır ve milyonlarca gereksiz renk değişkenini siler.
2. **Gauss Bulanıklaştırması (Gaussian Blurring):** Matematiksel bulanıklaştırma kullanarak sert piksel değişimlerini ve asfalttaki dokular, ufak çizikler gibi yüzey gürültülerini pürüzsüzleştirir.
3. **Canny Kenar Tespiti (Canny Edge Detection):** Piksel yoğunluğu gradyanlarını hesaplayarak plakanın yapısal sınırlarını ve oyuklarını belirginleştirir, düz arka plan silüetlerini ayıklar.
4. **Kontur Tespiti ve Kırpma (Contour Detection & Cropping):** Sürekli çizgileri analiz ederek plakanın dikdörtgen geometrik şeklini bulur, kesin koordinatlara kilitlenir ve ilgili bölgeyi ana resimden kırpar.
5. **OCR Metin Çıkarımı (OCR Extraction):** İzole edilmiş ve temizlenmiş plaka görüntüsünü **EasyOCR** kütüphanesi ile tarayarak terminale doğrudan makine tarafından okunabilir bir metin (string) çıktısı verir.

## 🚀 Kurulum ve Çalıştırma

### Gereksinimler
Bilgisayarınızda Python 3.8+ sürümünün kurulu olduğundan emin olun. Geliştirme ortamınızın varsayılan sanal ortamını (venv) kullanmanız şiddetle tavsiye edilir.

### 1. Depoyu Klonlayın
```bash
git clone [https://github.com/odabasberke/i2i-Academy-AppliedImageProcessing-1.git](https://github.com/odabasberke/i2i-Academy-AppliedImageProcessing-1.git)
cd i2i-Academy-AppliedImageProcessing-1
