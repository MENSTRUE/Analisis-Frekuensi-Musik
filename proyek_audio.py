# =============================================================================
# FINAL PROJECT PENGOLAHAN SINYAL DIGITAL
# Tema: Analisis Frekuensi Musik dengan GUI
#
# Deskripsi:
# Aplikasi ini memungkinkan pengguna untuk memuat file audio, memilih segmen
# tertentu, dan menganalisisnya dalam domain waktu dan frekuensi.
# Hasil analisis (Waveform, Spektrogram, dan Spektrum FFT) ditampilkan
# dan dapat diunduh sebagai file gambar.
#
# Library yang dibutuhkan:
# pip install tkinter pillow numpy scipy matplotlib librosa
# =============================================================================

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import librosa
import librosa.display
from scipy.fft import fft, fftfreq
import warnings

# Mengabaikan peringatan yang tidak kritikal dari librosa
warnings.filterwarnings('ignore')

# Mengatur style plot agar terlihat lebih modern
plt.style.use('seaborn-v0_8-whitegrid')


class AudioAnalyzerApp:
    """
    Kelas utama untuk aplikasi GUI Analisis Audio.
    """

    def __init__(self, root):
        self.root = root
        self.root.title("Final Project PSD - Analisis Frekuensi Musik")
        self.root.geometry("1200x800")

        # Variabel untuk menyimpan data audio dan path file
        self.audio_path = None
        self.y = None
        self.sr = None

        # Variabel untuk menyimpan figure Matplotlib
        self.fig_waveform = None
        self.fig_spectrogram = None
        self.fig_fft = None

        # --- Membuat Frame Utama ---
        # Frame untuk kontrol (atas)
        control_frame = ttk.Frame(root, padding="10")
        control_frame.pack(side=tk.TOP, fill=tk.X)

        # Frame untuk plot (tengah)
        self.plot_frame = ttk.Frame(root, padding="10")
        self.plot_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # --- Widget di Control Frame ---
        # Tombol Buka File
        self.btn_open = ttk.Button(control_frame, text="Buka File Audio", command=self.open_file)
        self.btn_open.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        # Label File
        self.lbl_file = ttk.Label(control_frame, text="File belum dipilih", width=40)
        self.lbl_file.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        # Input Waktu Mulai
        ttk.Label(control_frame, text="Waktu Mulai (detik):").grid(row=0, column=2, padx=5, pady=5, sticky="e")
        self.entry_start = ttk.Entry(control_frame, width=10)
        self.entry_start.grid(row=0, column=3, padx=5, pady=5)
        self.entry_start.insert(0, "0.0")

        # Input Waktu Akhir
        ttk.Label(control_frame, text="Waktu Akhir (detik):").grid(row=0, column=4, padx=5, pady=5, sticky="e")
        self.entry_end = ttk.Entry(control_frame, width=10)
        self.entry_end.grid(row=0, column=5, padx=5, pady=5)
        self.entry_end.insert(0, "5.0")

        # Tombol Analisis
        self.btn_analyze = ttk.Button(control_frame, text="Lakukan Analisis", command=self.analyze_segment)
        self.btn_analyze.grid(row=0, column=6, padx=10, pady=5, sticky="ew")

        # Konfigurasi grid agar responsif
        control_frame.grid_columnconfigure(1, weight=1)

        # --- Setup Area Plot ---
        self.setup_plot_areas()

    def setup_plot_areas(self):
        """Mempersiapkan frame untuk setiap plot dan tombol downloadnya."""
        # Konfigurasi grid di plot_frame
        self.plot_frame.grid_rowconfigure(1, weight=1)
        self.plot_frame.grid_columnconfigure(0, weight=1)
        self.plot_frame.grid_columnconfigure(1, weight=1)

        # Area Waveform
        frame_wave = ttk.LabelFrame(self.plot_frame, text="Waveform (Domain Waktu)")
        frame_wave.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")
        frame_wave.grid_rowconfigure(0, weight=1)
        frame_wave.grid_columnconfigure(0, weight=1)
        self.canvas_waveform = self.create_placeholder_canvas(frame_wave)
        ttk.Button(frame_wave, text="Download Grafik",
                   command=lambda: self.download_plot(self.fig_waveform, "waveform")).grid(row=1, column=0, pady=5)

        # Area Spektrogram
        frame_spec = ttk.LabelFrame(self.plot_frame, text="Spektrogram (STFT)")
        frame_spec.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
        frame_spec.grid_rowconfigure(0, weight=1)
        frame_spec.grid_columnconfigure(0, weight=1)
        self.canvas_spectrogram = self.create_placeholder_canvas(frame_spec)
        ttk.Button(frame_spec, text="Download Grafik",
                   command=lambda: self.download_plot(self.fig_spectrogram, "spectrogram")).grid(row=1, column=0,
                                                                                                 pady=5)

        # Area FFT
        frame_fft = ttk.LabelFrame(self.plot_frame, text="Spektrum Frekuensi (FFT)")
        frame_fft.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")
        frame_fft.grid_rowconfigure(0, weight=1)
        frame_fft.grid_columnconfigure(0, weight=1)
        self.canvas_fft = self.create_placeholder_canvas(frame_fft)
        ttk.Button(frame_fft, text="Download Grafik",
                   command=lambda: self.download_plot(self.fig_fft, "fft_spectrum")).grid(row=1, column=0, pady=5)

    def create_placeholder_canvas(self, parent):
        """Membuat canvas kosong sebagai placeholder sebelum analisis."""
        fig, ax = plt.subplots(figsize=(5, 4))
        ax.text(0.5, 0.5, "Hasil analisis akan muncul di sini", ha='center', va='center')
        ax.set_xticks([])
        ax.set_yticks([])
        canvas = FigureCanvasTkAgg(fig, master=parent)
        canvas.draw()
        canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")
        return canvas

    def open_file(self):
        """Membuka dialog untuk memilih file audio dan memuatnya."""
        self.audio_path = filedialog.askopenfilename(
            title="Pilih File Audio",
            filetypes=(("Audio Files", "*.wav *.mp3 *.m4a"), ("All files", "*.*"))
        )
        if not self.audio_path:
            return

        try:
            self.y, self.sr = librosa.load(self.audio_path)
            self.lbl_file.config(text=self.audio_path.split('/')[-1])
            messagebox.showinfo("Sukses", f"Berhasil memuat file.\nDurasi: {len(self.y) / self.sr:.2f} detik.")
        except Exception as e:
            messagebox.showerror("Error", f"Gagal memuat file audio: {e}")
            self.audio_path = None
            self.y = None
            self.sr = None

    def analyze_segment(self):
        """Fungsi utama untuk melakukan analisis pada segmen yang dipilih."""
        if self.y is None or self.sr is None:
            messagebox.showwarning("Peringatan", "Silakan buka file audio terlebih dahulu.")
            return

        try:
            start_time = float(self.entry_start.get())
            end_time = float(self.entry_end.get())
        except ValueError:
            messagebox.showerror("Error Input", "Waktu mulai dan akhir harus berupa angka.")
            return

        duration = len(self.y) / self.sr
        if not (0 <= start_time < end_time <= duration):
            messagebox.showerror("Error Waktu", f"Segmen waktu tidak valid. Harus antara 0 dan {duration:.2f} detik.")
            return

        # Konversi waktu ke indeks array
        start_sample = librosa.time_to_samples(start_time, sr=self.sr)
        end_sample = librosa.time_to_samples(end_time, sr=self.sr)
        y_segment = self.y[start_sample:end_sample]

        # Lakukan plotting
        self.plot_waveform(y_segment, self.sr)
        self.plot_spectrogram(y_segment, self.sr)
        self.plot_fft(y_segment, self.sr)

    def plot_waveform(self, y_data, sr_data):
        """Membuat dan menampilkan plot waveform."""
        self.fig_waveform, ax = plt.subplots(figsize=(10, 2))
        librosa.display.waveshow(y_data, sr=sr_data, ax=ax, alpha=0.8)
        ax.set_title("Waveform Sinyal Audio")
        ax.set_xlabel("Waktu (detik)")
        ax.set_ylabel("Amplitudo")
        self.fig_waveform.tight_layout()
        self.update_canvas(self.canvas_waveform, self.fig_waveform)

    def plot_spectrogram(self, y_data, sr_data):
        """Membuat dan menampilkan plot spektrogram."""
        self.fig_spectrogram, ax = plt.subplots(figsize=(5, 4))
        D = librosa.stft(y_data)
        DB = librosa.amplitude_to_db(np.abs(D), ref=np.max)
        img = librosa.display.specshow(DB, sr=sr_data, x_axis='time', y_axis='log', ax=ax)
        self.fig_spectrogram.colorbar(img, ax=ax, format='%+2.0f dB')
        ax.set_title("Spektrogram (STFT)")
        self.fig_spectrogram.tight_layout()
        self.update_canvas(self.canvas_spectrogram, self.fig_spectrogram)

    def plot_fft(self, y_data, sr_data):
        """Membuat dan menampilkan plot spektrum frekuensi (FFT)."""
        self.fig_fft, ax = plt.subplots(figsize=(5, 4))
        N = len(y_data)
        if N == 0: return  # Hindari error jika segmen kosong
        yf = fft(y_data)
        xf = fftfreq(N, 1 / sr_data)
        ax.plot(xf[:N // 2], 2.0 / N * np.abs(yf[:N // 2]))
        ax.set_title("Spektrum Frekuensi (FFT)")
        ax.set_xlabel("Frekuensi (Hz)")
        ax.set_ylabel("Amplitudo")
        ax.set_xlim(0, 5000)  # Batasi frekuensi agar mudah dilihat
        self.fig_fft.tight_layout()
        self.update_canvas(self.canvas_fft, self.fig_fft)

    def update_canvas(self, canvas_widget, new_figure):
        """Menghapus plot lama dan menggantinya dengan yang baru."""
        parent_frame = canvas_widget.get_tk_widget().master
        # Hapus widget canvas lama
        canvas_widget.get_tk_widget().destroy()
        # Buat canvas baru dengan figure baru
        new_canvas = FigureCanvasTkAgg(new_figure, master=parent_frame)
        new_canvas.draw()
        new_canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")
        # Simpan referensi ke canvas baru
        if canvas_widget == self.canvas_waveform:
            self.canvas_waveform = new_canvas
        elif canvas_widget == self.canvas_spectrogram:
            self.canvas_spectrogram = new_canvas
        elif canvas_widget == self.canvas_fft:
            self.canvas_fft = new_canvas

    def download_plot(self, figure, default_filename):
        """Menyimpan figure Matplotlib ke file gambar."""
        if figure is None:
            messagebox.showwarning("Peringatan", "Tidak ada grafik untuk diunduh. Lakukan analisis terlebih dahulu.")
            return

        filepath = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*")],
            initialfile=f"{default_filename}.png",
            title="Simpan Grafik Sebagai..."
        )

        if not filepath:
            return

        try:
            figure.savefig(filepath, dpi=300, bbox_inches='tight')
            messagebox.showinfo("Sukses", f"Grafik berhasil disimpan di:\n{filepath}")
        except Exception as e:
            messagebox.showerror("Error", f"Gagal menyimpan grafik: {e}")


if __name__ == "__main__":
    # Inisialisasi aplikasi Tkinter
    root = tk.Tk()
    app = AudioAnalyzerApp(root)
    root.mainloop()
