// # lib/src/features/authentication/domain/auth_repository.dart

// # Ini adalah kelas abstrak, seperti sebuah "kontrak" atau "blueprint".
// # Ia memberi tahu bagian lain dari aplikasi (seperti BLoC) bahwa
// # "Siapapun yang mengimplementasikan AuthRepository HARUS memiliki fungsi login".
// # Tapi ia tidak peduli BAGAIMANA cara login itu dilakukan (apakah lewat API,
// # database lokal, dll).

abstract class AuthRepository {
  // # Kontraknya adalah ada fungsi login yang menerima email dan password.
  // # Future<void> berarti fungsi ini adalah operasi asynchronous yang
  // # tidak mengembalikan data spesifik jika berhasil, tapi bisa melempar error jika gagal.
  Future<void> login(String email, String password);

  // # TODO: Nanti kita tambahkan kontrak lain di sini, seperti:
  // # Future<void> register(String name, String email, String password);
  // # Future<void> logout();
  // # Future<void> forgotPassword(String email);
}