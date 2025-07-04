// # lib/src/modules/authentication/presentation/bloc/auth_event.dart
part of 'auth_bloc.dart'; // <-- BARIS INI SANGAT PENTING

@immutable
abstract class AuthEvent {}

class LoginButtonPressed extends AuthEvent {
  final String email;
  final String password;
  LoginButtonPressed({required this.email, required this.password});
}