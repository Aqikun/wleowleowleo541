// -- KODE UNTUK INTERAKSI LANJUTAN --
// -- FILE: lib/src/features/authentication/presentation/bloc/auth_bloc.dart --

import 'package:bloc/bloc.dart';
import 'package:equatable/equatable.dart';
import 'package:frontend/src/shared/domain/exceptions/auth_exceptions.dart';
import 'package:frontend/src/features/authentication/domain/auth_repository.dart';

// Penting: Pastikan file event dan state Anda diimpor dengan benar
part 'auth_event.dart';
part 'auth_state.dart';

class AuthBloc extends Bloc<AuthEvent, AuthState> {
  final AuthRepository _authRepository;

  AuthBloc({required AuthRepository authRepository})
      : _authRepository = authRepository,
        super(AuthInitial()) {
    on<LoginButtonPressed>(_onLoginButtonPressed);
    on<RegisterButtonPressed>(_onRegisterButtonPressed);
    // Tambahkan handler untuk event logout nanti
  }

  Future<void> _onLoginButtonPressed(
    LoginButtonPressed event,
    Emitter<AuthState> emit,
  ) async {
    emit(AuthLoading());
    try {
      await _authRepository.login(event.email, event.password);
      // === PERUBAHAN UTAMA DI SINI ===
      // Mengeluarkan state yang lebih spesifik untuk login sukses
      emit(AuthLoginSuccess());
      // ==============================
    } on InvalidCredentialsException {
      emit(const AuthFailure(message: 'Email atau password salah.'));
    } on NetworkException {
      emit(const AuthFailure(message: 'Tidak ada koneksi internet.'));
    } catch (e) {
      emit(AuthFailure(message: 'Terjadi kesalahan: ${e.toString()}'));
    }
  }

  Future<void> _onRegisterButtonPressed(
    RegisterButtonPressed event,
    Emitter<AuthState> emit,
  ) async {
    emit(RegisterLoading());
    try {
      await _authRepository.register(
        ownerName: event.ownerName,
        businessName: event.businessName,
        email: event.email,
        password: event.password,
      );
      emit(RegisterSuccess());
    } on EmailAlreadyInUseException {
      emit(const RegisterFailure(
          message: 'Email yang Anda masukkan sudah terdaftar.'));
    } on NetworkException {
      emit(const RegisterFailure(message: 'Tidak ada koneksi internet.'));
    } catch (e) {
      emit(RegisterFailure(message: 'Registrasi gagal: ${e.toString()}'));
    }
  }
}