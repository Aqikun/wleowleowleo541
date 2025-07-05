// lib/src/shared/domain/exceptions/auth_exceptions.dart

/// Exception umum untuk masalah jaringan.
class NetworkException implements Exception {
  const NetworkException();
}

/// Exception ketika kredensial login tidak valid.
class InvalidCredentialsException implements Exception {
  const InvalidCredentialsException();
}

/// Exception ketika email sudah digunakan saat registrasi.
class EmailAlreadyInUseException implements Exception {
  const EmailAlreadyInUseException();
}