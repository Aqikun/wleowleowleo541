// # lib/src/modules/authentication/domain/auth_repository.dart
abstract class AuthRepository {
  Future<void> login(String email, String password);
}