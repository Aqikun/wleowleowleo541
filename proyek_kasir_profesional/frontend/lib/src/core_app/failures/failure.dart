// lib/src/core_app/failures/failure.dart
class Failure {
  final String message;
  Failure(this.message);
  @override
  String toString() => message;
}