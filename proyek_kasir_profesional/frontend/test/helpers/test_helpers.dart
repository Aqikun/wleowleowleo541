// test/helpers/test_helpers.dart

import 'package:bloc_test/bloc_test.dart';
import 'package:frontend/src/features/authentication/presentation/bloc/auth_bloc.dart'; // Sesuaikan path jika perlu

// Gunakan MockBloc dari package bloc_test untuk setup yang lebih mudah
class MockAuthBloc extends MockBloc<AuthEvent, AuthState> implements AuthBloc {}