// # lib/src/core/api_client.dart

import 'package:dio/dio.dart';

class ApiClient {
  // # Buat instance dio yang akan kita gunakan di seluruh aplikasi
  final Dio dio;

  ApiClient()
      : dio = Dio(
          BaseOptions(
            // # TODO: Ganti dengan alamat IP atau domain backend Anda
            // # Jika menjalankan backend di komputer yang sama, gunakan 10.0.2.2 untuk Android Emulator
            // # atau alamat IP lokal Anda (misal: http://192.168.1.5:8000) jika menggunakan perangkat fisik.
            baseUrl: 'http://10.0.2.2:8000/api/v1',
            connectTimeout: const Duration(milliseconds: 5000), // 5 detik
            receiveTimeout: const Duration(milliseconds: 3000), // 3 detik
            headers: {
              'Accept': 'application/json',
            },
          ),
        ) {
    // # Di sini kita bisa menambahkan interceptor untuk logging,
    // # penanganan token otomatis, dll.
    dio.interceptors.add(
      LogInterceptor(
        requestBody: true,
        responseBody: true,
      ),
    );
  }
}