// # lib/src/features/authentication/infrastructure/auth_repository_impl.dart

import 'package:dio/dio.dart';
import 'package:frontend/src/core/api_client.dart'; // # Ganti 'frontend' dengan nama proyek Anda
import 'package:frontend/src/features/authentication/domain/auth_repository.dart'; // # Ganti 'frontend' dengan nama proyek Anda

// # Kelas ini adalah implementasi NYATA dari AuthRepository.
// # Dia "berjanji" untuk memenuhi semua kontrak yang ada di AuthRepository.
class AuthRepositoryImpl implements AuthRepository {
  // # Kita butuh ApiClient untuk bisa berbicara dengan internet.
  final ApiClient _apiClient;

  // # Constructor: Saat AuthRepositoryImpl dibuat, ia harus diberi ApiClient.
  AuthRepositoryImpl(this._apiClient);

  // # Ini adalah implementasi dari fungsi login yang ada di kontrak.
  @override
  Future<void> login(String email, String password) async {
    try {
      // # Data yang akan dikirim sebagai body request ke API.
      final data = {
        'username': email, // # Sesuai standar OAuth2, username biasanya adalah email
        'password': password,
      };

      // # Memanggil endpoint login di backend menggunakan dio dari ApiClient.
      // # Kita menggunakan FormData karena endpoint token OAuth2 biasanya
      // # mengharapkan format x-www-form-urlencoded, bukan JSON.
      await _apiClient.dio.post(
        '/auth/token', // # Sesuaikan dengan path endpoint login Anda
        data: FormData.fromMap(data),
      );

      // # TODO: Jika login berhasil, API akan mengembalikan token.
      // # Kita perlu menyimpan token ini (misal: di SharedPreferences)
      // # untuk digunakan di request API selanjutnya.

    } on DioException catch (e) {
      // # Jika terjadi error dari dio (misal: server tidak merespon,
      // # atau server mengembalikan status 400/500), kita tangkap di sini.
      // # Kita bisa membuat pesan error yang lebih mudah dimengerti.
      // # Lalu kita lempar lagi error-nya agar bisa ditangkap oleh BLoC/UI.
      print('Error on login: $e');
      throw Exception('Gagal melakukan login. Periksa kembali email dan password Anda.');
    } catch (e) {
      // # Menangkap error lain yang mungkin terjadi.
      print('Unexpected error on login: $e');
      throw Exception('Terjadi kesalahan yang tidak terduga.');
    }
  }
}