# Dokumentasi Menjalankan FastAPI

Dokumentasi ini berisi langkah-langkah untuk menjalankan proyek FastAPI dengan benar.

## Menjalankan FastAPI

### 1. Membuat Virtual Environment
Sebelum menjalankan proyek, buat virtual environment terlebih dahulu.

```sh
conda --name venv 
```

Aktifkan virtual environment:
- **Windows:**
  ```sh
  conda activate venv
  ```

### 2. Menginstal Dependensi
Setelah virtual environment aktif, instal semua library yang diperlukan:

```sh
pip install -r requirements.txt
```

### 3. Menjalankan Server FastAPI
Gunakan Uvicorn untuk menjalankan server:

- Dengan port 8000:
  ```sh
  uvicorn main:app --reload
  ```

## Endpoint API
Dokumentasi API dapat diakses setelah server berjalan.

Untuk melihat dokumentasi lebih lengkap, silakan buka:
- `http://localhost/docs` untuk Swagger UI
- `http://localhost/redoc` untuk ReDoc

---

**Catatan:**
- Pastikan `requirements.txt` telah diperbarui dengan semua dependensi yang dibutuhkan.
- Pastikan Anda menggunakan Python versi yang sesuai dengan proyek ini.

Selamat coding! 🚀

    