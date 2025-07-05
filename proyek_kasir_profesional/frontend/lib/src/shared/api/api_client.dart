// lib/src/shared/api/api_client.dart

import 'package:dio/dio.dart';

class ApiClient {
  final Dio dio;

  ApiClient()
      : dio = Dio(
          BaseOptions(
            baseUrl: 'http://127.0.0.1:8000/api/', // Pastikan ada /api/ di akhir jika itu path utama API Anda
            connectTimeout: const Duration(milliseconds: 5000),
            receiveTimeout: const Duration(milliseconds: 3000),
            headers: {'Accept': 'application/json'},
          ),
        ) {
    // LogInterceptor Anda yang sudah ada dipertahankan, ini bagus untuk debugging.
    dio.interceptors.add(
      LogInterceptor(
        requestBody: true,
        responseBody: true,
      ),
    );
  }

  /// Melakukan permintaan GET ke [path] yang diberikan.
  Future<Response> get(String path) async {
    try {
      final response = await dio.get(path);
      return response;
    } on DioException catch (e) {
      // Melempar kembali error agar bisa ditangani di lapisan repository
      throw _handleError(e);
    }
  }

  /// Melakukan permintaan POST ke [path] dengan [data] yang diberikan.
  Future<Response> post(String path, {dynamic data}) async {
    try {
      final response = await dio.post(path, data: data);
      return response;
    } on DioException catch (e) {
      throw _handleError(e);
    }
  }

  /// Helper untuk mengubah DioException menjadi Exception yang lebih mudah dibaca.
  Exception _handleError(DioException e) {
    final errorResponse = e.response;
    if (errorResponse != null) {
      // Jika server memberikan response error (spt. 404, 500, 422)
      final errorMessage = errorResponse.data?['message'] ?? 'Terjadi kesalahan';
      return Exception('Error: ${errorResponse.statusCode} - $errorMessage');
    } else {
      // Jika terjadi error koneksi atau lainnya
      return Exception('Gagal terhubung ke server: ${e.message}');
    }
  }
}