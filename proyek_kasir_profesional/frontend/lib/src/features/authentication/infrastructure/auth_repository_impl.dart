// lib/src/features/authentication/infrastructure/auth_repository_impl.dart

import 'package:frontend/src/features/authentication/domain/auth_repository.dart';
// // KEMUNGKINAN BESAR INI ADALAH SUMBER MASALAHNYA
// // Saya berasumsi file ini sekarang berada di bawah `features` atau `core_app`
// // Jika path ini masih salah, tolong berikan saya struktur folder Anda
import 'package:frontend/src/shared/api/api_client.dart'; // PERBAIKAN JALUR IMPORT

class AuthRepositoryImpl implements AuthRepository {
  final ApiClient _apiClient;

  AuthRepositoryImpl(this._apiClient);

  @override
  Future<void> login(String email, String password) async {
    // Implementasi login
    try {
      await _apiClient.post(
        '/auth/token',
        data: {
          'username': email,
          'password': password,
        },
      );
    } catch (e) {
      rethrow;
    }
  }

  @override
  Future<void> register({
    required String ownerName,
    required String businessName,
    required String email,
    required String password,
  }) async {
    try {
      await _apiClient.post(
        '/auth/register',
        data: {
          'owner_name': ownerName,
          'business_name': businessName,
          'email': email,
          'password': password,
        },
      );
    } catch (e) {
      rethrow;
    }
  }

  @override
  Future<void> forgotPassword(String email) async {
    // Implementasi lupa password
  }
}