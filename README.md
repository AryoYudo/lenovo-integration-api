# 📌 Dokumentasi API SFIS

Dokumentasi ini berisi daftar endpoint API untuk sistem SFIS. Setiap request memerlukan **Authorization** yang harus dikirim dalam header (bukan Bearer Auth).

## 🚀 Menjalankan FastAPI

1. Masuk ke direktori project.
2. Aktifkan virtual environment:
   ```sh
   source venv/bin/activate  # Untuk Linux/Mac
   venv\Scripts\activate  # Untuk Windows
   ```
3. Pindah ke direktori `mysatnusa`:
   ```sh
   cd mysatnusa
   ```
4. Jalankan server menggunakan Uvicorn:
   ```sh
   uvicorn core.main:app --port=8080
   ```

## 🔐 Autentikasi
Setiap endpoint memerlukan header `Authorization` dengan token yang didapat dari endpoint login.

## 📌 Endpoint API

### 1️⃣ Login
**URL:** `http://127.0.0.1:8080/sfis/login`

**Metode:** `POST`

**Body:**
```json
{
    "username": "test", 
    "password": "11",
    "device_name": " DSY_Test_1002",
    "station_name": "Autoscrew"
}
```

---

### 2️⃣ Incoming Part
**URL:** `http://127.0.0.1:8080/sfis/insert_solder`

**Metode:** `POST`

**Body:**
```json
{
    "scan_item": "P45001412546AD24072000000098",
    "data_name": "ISN",
    "qty_per_batch": 4,
    "device_name": "Device_ABC",
    "station_name": "Station_123",
    "key_item": "P45001412546AD24072000000098",
    "is_pass": true,
    "log_path": "",
    "work_order_no": ""
}
```

---

### 3️⃣ Check Route Batch
**URL:** `http://127.0.0.1:8080/sfis/insert_check_router`

**Metode:** `POST`

**Body:**
```json
{
    "key_item": "P45001412546AD24072000000098",
    "station_name": "ISN_INPUT",
    "device_name": "DSY_Test_1001",
    "is_pass": true,        
    "error_code": "",        
    "log_path": "",        
    "log_data": "",        
    "scan_item": "",
    "data_name": ""
}
```