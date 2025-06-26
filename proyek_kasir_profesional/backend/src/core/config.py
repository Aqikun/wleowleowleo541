# backend/src/core/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict

# Kelas Settings digunakan untuk mengelola semua konfigurasi aplikasi.
class Settings(BaseSettings):
    # Kelas ini akan membaca variabel dari file .env secara otomatis.
    
    # Pengaturan untuk koneksi Database
    DATABASE_URL: str
    TEST_DATABASE_URL: str

    # Pengaturan untuk keamanan otentikasi menggunakan JWT
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Konfigurasi model untuk menunjuk ke file .env sebagai sumber variabel
    model_config = SettingsConfigDict(env_file=".env")

# 'settings' adalah sebuah instance dari kelas Settings.
# Objek ini akan diimpor dan digunakan di seluruh bagian aplikasi
# untuk mengakses nilai konfigurasi.
settings = Settings()
