// lib/src/features/authentication/presentation/bloc/auth_event.dart

part of 'auth_bloc.dart';

abstract class AuthEvent extends Equatable {
  const AuthEvent();

  @override
  List<Object> get props => [];
}

class LoginButtonPressed extends AuthEvent {
  final String email;
  final String password;

  const LoginButtonPressed({
    required this.email,
    required this.password,
  });

  @override
  List<Object> get props => [email, password];
}

class RegisterButtonPressed extends AuthEvent {
  final String ownerName;
  final String businessName;
  final String email;
  final String password;

  const RegisterButtonPressed({
    required this.ownerName,
    required this.businessName,
    required this.email,
    required this.password,
  });

  @override
  List<Object> get props => [ownerName, businessName, email, password];
}