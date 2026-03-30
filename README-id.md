# text-generator

Generator teks uji, dipermudah.

## Pendahuluan

Repo ini adalah versi yang ditingkatkan dari [Just Another Test Text Generator](http://justanotherfoundry.com/generator). Kode ini memungkinkan pembuatan teks yang terlihat alami untuk pengujian font, menggunakan analisis trigram dari berbagai korpus bahasa.

Versi ini menyertakan port Google Colab dan aplikasi web mandiri untuk memudahkan penggunaan di lingkungan modern.

## Fitur

1. **Konversi Korpus ke Trigram**: Ubah teks apa pun menjadi format TSV trigram yang digunakan oleh generator.
2. **Pembuatan Teks Deterministik**: Menghasilkan teks dengan seed acak yang tetap untuk hasil yang dapat diulang.
3. **Paritas Fitur Lengkap**: Mendukung penyesuaian variasi huruf, variasi pasangan, dan penyesuaian probabilitas berbasis kerning.
4. **Alat Berbasis Browser**: Termasuk `generator.html` untuk pembuatan teks langsung di browser menggunakan file TSV yang diunggah.
5. **Notebook Colab**: Termasuk `text_generator.ipynb` untuk alur kerja yang mudah di cloud.

## Detail Teknis

### Analisis Trigram

Generator menggunakan statistik trigram untuk memprediksi karakter berikutnya berdasarkan dua karakter sebelumnya. Spasi diwakili oleh karakter garis bawah (`_`).

### Faktor Penyesuaian (Tweaks)

*   **Letter Variety**: Menyeimbangkan frekuensi huruf agar distribusi karakter lebih merata.
*   **Pair Variety**: Menyeimbangkan frekuensi pasangan karakter.
*   **Word Length Biasing**: Menyesuaikan probabilitas spasi untuk mengikuti distribusi panjang kata yang ditemukan di korpus asli.
*   **Kerning**: Menggunakan data dari `kerning.txt` untuk menyesuaikan probabilitas berdasarkan pasangan kerning tipikal.

## Cara Penggunaan

### Menggunakan Google Colab

Buka `text_generator.ipynb` di Google Colab untuk mengonversi teks korpus Anda sendiri atau menghasilkan teks dari data yang ada.

### Menggunakan Web Browser

Buka `generator.html` di browser apa pun. Unggah file TSV trigram (Anda dapat menemukannya di direktori `languages/`) dan klik "Generate Text".

### Menggunakan Skrip Python

Jalankan skrip generator asli:
```bash
python3 scripts/generator.py -language en -characters all -kern typ -kernlevel 0 -lettervariety 0 -pairvariety 0 -case normal
```

## Lisensi

Lisensi Publik Umum GNU v2.0. Berdasarkan kode asli oleh Tim Ahrens ([Just Another Foundry](http://justanotherfoundry.com/)).
