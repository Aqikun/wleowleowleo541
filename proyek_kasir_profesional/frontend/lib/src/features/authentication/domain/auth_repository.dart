// lib/src/features/authentication/domain/auth_repository.dart

abstract class AuthRepository {
  Future<void> login(String email, String password);

  Future<void> register({
    required String ownerName,
    required String businessName,
    required String email,
    required String password,
  });

  Future<void> forgotPassword(String email);
}