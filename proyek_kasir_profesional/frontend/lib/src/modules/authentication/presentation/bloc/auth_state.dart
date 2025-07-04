// # lib/src/modules/authentication/presentation/bloc/auth_state.dart
part of 'auth_bloc.dart'; // <-- BARIS INI SANGAT PENTING

@immutable
abstract class AuthState {}

class AuthInitial extends AuthState {}

class AuthLoading extends AuthState {}

class AuthSuccess extends AuthState {}

class AuthFailure extends AuthState {
  final String error;
  AuthFailure({required this.error});
}