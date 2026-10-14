# Mining Control Room (MCR) Operation Toolkit — Portfolio Website

Website portofolio statis ini menyajikan studi kasus otomatisasi validasi timesheet dan monitoring unit alat berat di sektor pertambangan.

## Cara Mengunggah ke GitHub Pages

Ikuti langkah-langkah berikut untuk mempublikasikan halaman portofolio ini secara gratis melalui GitHub Pages:

1. **Buat Repository Baru di GitHub**:
   - Buka [GitHub](https://github.com) dan login ke akun Anda.
   - Klik tombol **New** (atau ikon `+` di pojok kanan atas) untuk membuat repository baru.
   - Beri nama repository, misalnya: `mcr-operation-toolkit`.
   - Pilih visibilitas **Public** (wajib untuk GitHub Pages gratis).
   - *Jangan* centang "Add a README file" (karena kita sudah memilikinya secara lokal).
   - Klik **Create repository**.

2. **Inisialisasi Git & Upload File ke GitHub**:
   Buka terminal (PowerShell atau Bash) di folder tempat file `index.html` dan `README.md` berada (`C:\Users\muham`), lalu jalankan perintah berikut:

   ```bash
   git init
   git add index.html README.md
   git commit -m "Initial commit: MCR Operation Toolkit portfolio landing page"
   git branch -M main
   git remote add origin https://github.com/USERNAME/mcr-operation-toolkit.git
   git push -u origin main
   ```
   *(Catatan: Ganti `USERNAME` dengan username GitHub Anda dan `mcr-operation-toolkit` dengan nama repository Anda).*

3. **Aktifkan GitHub Pages**:
   - Buka repository Anda di browser web GitHub.
   - Masuk ke tab **Settings** (Pengaturan repository).
   - Di menu sebelah kiri, klik **Pages**.
   - Pada bagian **Build and deployment** -> **Branch**, pilih branch `main` (atau `master`) dan folder `/ (root)`.
   - Klik **Save**.

4. **Selesai!**
   Dalam waktu 1-2 menit, GitHub akan mempublikasikan situs Anda. URL live website portofolio Anda akan muncul di bagian atas halaman Settings > Pages (biasanya berformat `https://USERNAME.github.io/mcr-operation-toolkit/`).
