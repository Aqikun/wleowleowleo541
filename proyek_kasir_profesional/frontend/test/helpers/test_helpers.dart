// test/helpers/test_helpers.dart
import 'package:bloc_test/bloc_test.dart';
import 'package:frontend/src/features/authentication/presentation/bloc/auth_bloc.dart';
import 'package:frontend/src/features/retail/product/presentation/bloc/product_bloc.dart';

class MockAuthBloc extends MockBloc<AuthEvent, AuthState> implements AuthBloc {}
class MockProductBloc extends MockBloc<ProductEvent, ProductState> implements ProductBloc {}