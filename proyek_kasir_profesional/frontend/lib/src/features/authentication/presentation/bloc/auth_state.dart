// -- KODE UNTUK INTERAKSI LANJUTAN --
// -- FILE: lib/src/features/authentication/presentation/bloc/auth_state.dart --

part of 'auth_bloc.dart';

abstract class AuthState extends Equatable {
  const AuthState();

  @override
  List<Object> get props => [];
}

class AuthInitial extends AuthState {}

// State untuk proses Login
class AuthLoading extends AuthState {}

class AuthSuccess extends AuthState {} // State umum, bisa kita gunakan nanti

// === PENAMBAHAN KELAS YANG HILANG DI SINI ===
// State spesifik untuk menandakan login telah berhasil.
// Ini akan menjadi sinyal bagi UI untuk melakukan navigasi.
class AuthLoginSuccess extends AuthState {}
// ===========================================

class AuthFailure extends AuthState {
  final String message;

  const AuthFailure({required this.message});

  @override
  List<Object> get props => [message];
}

// State untuk proses Register
class RegisterLoading extends AuthState {}

class RegisterSuccess extends AuthState {}

class RegisterFailure extends AuthState {
  final String message;

  const RegisterFailure({required this.message});

  @override
  List<Object> get props => [message];
}