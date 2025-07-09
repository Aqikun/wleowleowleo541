// -- KODE UNTUK INTERAKSI LANJUTAN --
// -- FILE: lib/src/shared/api/api_client.dart --

import 'package:dio/dio.dart';

// TODO: Nanti kita akan integrasikan dengan flutter_secure_storage
// import 'package:flutter_secure_storage/flutter_secure_storage.dart';

class ApiClient {
  final Dio dio;
  // TODO: Nanti kita akan gunakan ini untuk menyimpan token
  // final _storage = const FlutterSecureStorage();

  // Variabel statis untuk menyimpan token sementara selama sesi aplikasi
  static String? _token;

  ApiClient()
      : dio = Dio(
          BaseOptions(
            baseUrl: 'http://127.0.0.1:8000/api/v1/',
            connectTimeout: const Duration(milliseconds: 5000),
            receiveTimeout: const Duration(milliseconds: 3000),
            headers: {'Accept': 'application/json'},
          ),
        ) {
    dio.interceptors.add(
      LogInterceptor(
        requestBody: true,
        responseBody: true,
      ),
    );

    // === INTERCEPTOR UNTUK OTENTIKASI ===
    dio.interceptors.add(
      InterceptorsWrapper(
        onRequest: (options, handler) async {
          // TODO: Ganti logika ini dengan membaca token dari FlutterSecureStorage
          // final String? token = await _storage.read(key: 'auth_token');

          // Untuk saat ini, kita gunakan variabel statis
          final String? token = ApiClient._token;

          if (token != null && token.isNotEmpty) {
            options.headers['Authorization'] = 'Bearer $token';
          }
          return handler.next(options); // Lanjutkan permintaan
        },
        onError: (DioException e, handler) async {
          // TODO: Tambahkan logika untuk refresh token jika diperlukan nanti
          return handler.next(e);
        },
      ),
    );
  }

  // Metode untuk menyimpan token setelah login berhasil
  static void setToken(String? token) {
    _token = token;
    // TODO: Nanti kita juga simpan ke FlutterSecureStorage
    // if (token != null) {
    //   await _storage.write(key: 'auth_token', value: token);
    // } else {
    //   await _storage.delete(key: 'auth_token');
    // }
  }


  // ... sisa kode tidak perlu diubah ...
  Future<Response> get(String path) async {
    try {
      final response = await dio.get(path);
      return response;
    } on DioException catch (e) {
      throw _handleError(e);
    }
  }

  Future<Response> post(String path, {dynamic data, Options? options}) async {
    try {
      final response = await dio.post(path, data: data, options: options);
      return response;
    } on DioException catch (e) {
      throw _handleError(e);
    }
  }

  Future<Response> put(String path, {dynamic data}) async {
    try {
      final response = await dio.put(path, data: data);
      return response;
    } on DioException catch (e) {
      throw _handleError(e);
    }
  }

  Future<Response> delete(String path) async {
    try {
      final response = await dio.delete(path);
      return response;
    } on DioException catch (e) {
      throw _handleError(e);
    }
  }

  Exception _handleError(DioException e) {
    final errorResponse = e.response;
    if (errorResponse != null) {
      final errorMessage = errorResponse.data?['message'] ?? 'Terjadi kesalahan';
      return Exception('Error: ${errorResponse.statusCode} - $errorMessage');
    } else {
      return Exception('Gagal terhubung ke server: ${e.message}');
    }
  }
}