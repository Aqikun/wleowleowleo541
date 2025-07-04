// # lib/src/modules/authentication/infrastructure/auth_repository_impl.dart
import 'package:dio/dio.dart';
import 'package:frontend/src/shared/api/api_client.dart';
import 'package:frontend/src/modules/authentication/domain/auth_repository.dart';

class AuthRepositoryImpl implements AuthRepository {
  final ApiClient _apiClient;

  AuthRepositoryImpl(this._apiClient);

  @override
  Future<void> login(String email, String password) async {
    try {
      final data = {
        'username': email,
        'password': password,
      };
      await _apiClient.dio.post(
        '/auth/token', // Sesuaikan dengan endpoint login Anda
        data: FormData.fromMap(data),
      );
    } on DioException catch (e) {
      print('Error on login: $e');
      throw Exception('Gagal login. Periksa kembali email dan password Anda.');
    } catch (e) {
      print('Unexpected error on login: $e');
      throw Exception('Terjadi kesalahan yang tidak terduga.');
    }
  }
}