// lib/src/shared/api/api_client.dart

import 'package:dio/dio.dart';

class ApiClient {
  final Dio dio;

  ApiClient()
      : dio = Dio(
          BaseOptions(
            // PASTIKAN ALAMAT INI BENAR
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

  Future<Response> post(String path, {dynamic data}) async {
    try {
      final response = await dio.post(path, data: data);
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