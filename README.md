Aplikasi Analisis Frekuensi Musik
Aplikasi desktop sederhana berbasis Python untuk menganalisis sinyal audio dalam domain waktu dan frekuensi. Proyek ini dibuat untuk memenuhi tugas akhir mata kuliah Pengolahan Sinyal Digital (PSD).

🎵 Tentang Proyek
Aplikasi ini memungkinkan pengguna untuk memuat file audio (seperti .wav, .mp3, atau .m4a), memilih segmen waktu tertentu, dan melakukan analisis fundamental Pengolahan Sinyal Digital. Hasil analisis divisualisasikan dalam tiga plot utama: Waveform, Spektrogram (STFT), dan Spektrum Frekuensi (FFT). Setiap plot yang dihasilkan dapat diunduh sebagai file gambar (.png) untuk keperluan laporan atau analisis lebih lanjut.

Proyek ini mengimplementasikan konsep-konsep kunci PSD, termasuk representasi sinyal domain waktu, transformasi Fourier, dan analisis waktu-frekuensi.

✨ Fitur Utama
GUI Interaktif: Antarmuka yang mudah digunakan berbasis Tkinter.

Memuat Berbagai Format Audio: Mendukung format audio umum berkat library librosa.

Seleksi Segmen Audio: Pengguna dapat menentukan rentang waktu (dalam detik) yang ingin dianalisis.

Visualisasi Multi-Plot:

Waveform: Amplitudo vs. Waktu.

Spektrogram: Analisis STFT untuk melihat bagaimana frekuensi berubah seiring waktu.

Spektrum Frekuensi: Analisis FFT untuk melihat komponen frekuensi dominan.

Unduh Grafik: Opsi untuk menyimpan setiap plot sebagai file gambar berkualitas tinggi.

🛠️ Teknologi yang Digunakan
Python 3.11

Tkinter: Untuk membangun antarmuka grafis (GUI).

Librosa: Untuk memuat dan memproses sinyal audio.

Matplotlib: Untuk membuat dan menampilkan plot/grafik.

NumPy & SciPy: Untuk komputasi numerik dan algoritma FFT.

🚀 Cara Menjalankan
Berikut adalah langkah-langkah untuk menyiapkan dan menjalankan proyek ini di komputer lokal Anda.

1. Prasyarat
Pastikan Anda sudah menginstal Python versi 3.8 atau lebih baru.

2. Kloning atau Unduh Proyek
Unduh atau kloning repositori ini ke mesin lokal Anda.

3. Buat dan Aktifkan Virtual Environment
Sangat disarankan untuk menggunakan virtual environment agar dependensi proyek tidak tercampur dengan instalasi Python global Anda.

Buka terminal di dalam folder proyek, lalu jalankan:

# Membuat virtual environment (hanya sekali)
python -m venv .venv

# Mengaktifkan virtual environment
# Windows (PowerShell)
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate

4. Instal Dependensi
Dengan virtual environment yang sudah aktif, instal semua library yang dibutuhkan:

pip install tkinter pillow numpy scipy matplotlib librosa

5. Jalankan Aplikasi
Setelah semua dependensi terinstal, jalankan aplikasi dengan perintah:

python proyek_audio.py

Jendela aplikasi akan muncul dan siap digunakan.

📖 Cara Penggunaan
Klik tombol "Buka File Audio" untuk memilih file musik dari komputer Anda.

Masukkan waktu mulai dan akhir (dalam detik) pada kolom yang tersedia untuk memilih segmen yang ingin dianalisis.

Klik tombol "Lakukan Analisis". Tiga plot akan muncul di jendela.

Untuk menyimpan, klik tombol "Download Grafik" di bawah masing-masing plot.
