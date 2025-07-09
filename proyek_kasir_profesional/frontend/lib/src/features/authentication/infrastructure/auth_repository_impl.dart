// -- KODE UNTUK INTERAKSI LANJUTAN --
// -- FILE: lib/src/features/authentication/infrastructure/auth_repository_impl.dart --

import 'package:dio/dio.dart';
import 'package:frontend/src/features/authentication/domain/auth_repository.dart';
import 'package:frontend/src/shared/api/api_client.dart';
import 'package:frontend/src/shared/domain/exceptions/auth_exceptions.dart';

class AuthRepositoryImpl implements AuthRepository {
  final ApiClient _apiClient;

  AuthRepositoryImpl(this._apiClient);

  @override
  Future<void> login(String email, String password) async {
    try {
      final response = await _apiClient.post(
        '/token', // Path sudah benar
        // Mengirim data sebagai form, bukan JSON, sesuai standar OAuth2
        data: FormData.fromMap({
          'username': email, // Backend mengharapkan 'username'
          'password': password,
        }),
        options: Options(
          // Set content type yang benar
          contentType: 'application/x-www-form-urlencoded',
        ),
      );

      // === PERUBAHAN UTAMA DI SINI ===
      // Memeriksa apakah login sukses dan ada data yang diterima
      if (response.statusCode == 200 && response.data != null) {
        // Ambil access_token dari respons JSON
        final String token = response.data['access_token'];
        
        // Simpan token menggunakan metode statis yang ada di ApiClient
        ApiClient.setToken(token);

        // TODO: Nanti kita juga akan menyimpan data 'user' dari respons
        // ke dalam state management (misalnya AuthBloc) agar bisa diakses
        // di seluruh aplikasi, seperti untuk menampilkan nama di HomeScreen.
      }
      // ==============================

    } on DioException catch (e) {
      // Jika status code adalah 401, artinya kredensial salah
      if (e.response?.statusCode == 401) {
        throw const InvalidCredentialsException();
      }
      // Untuk error jaringan lainnya
      throw const NetworkException();
    } catch (e) {
      // Untuk error tak terduga lainnya
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
      // Endpoint register masih menggunakan JSON, ini sudah benar
      await _apiClient.post(
        '/register',
        data: {
          // Sesuaikan key ini dengan yang diharapkan oleh Pydantic schema di backend
          // 'username' bisa diambil dari nama bisnis atau nama pemilik
          'username': businessName,
          'email': email,
          'password': password,
          'role': 'Owner', // Di-hardcode sebagai Owner saat registrasi awal
          'phone_number': '' // Placeholder, bisa diisi nanti
        },
      );
    } on DioException catch (e) {
      // Cek jika error karena email/username sudah terdaftar
      if (e.response?.data['detail']?.toString().contains('already registered') ?? false) {
        throw const EmailAlreadyInUseException();
      }
      throw const NetworkException();
    } catch (e) {
      rethrow;
    }
  }

  @override
  Future<void> forgotPassword(String email) async {
    // Implementasi lupa password bisa ditambahkan di sini nanti
  }
}