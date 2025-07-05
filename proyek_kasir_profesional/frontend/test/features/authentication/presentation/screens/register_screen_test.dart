// test/features/authentication/presentation/screens/register_screen_test.dart

import 'package:bloc_test/bloc_test.dart';
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:frontend/src/features/authentication/presentation/bloc/auth_bloc.dart';
import 'package:frontend/src/features/authentication/presentation/screens/register_screen.dart';

import '../../../../helpers/test_helpers.dart';

void main() {
  group('RegisterScreen', () {
    late AuthBloc mockAuthBloc;

    setUp(() {
      mockAuthBloc = MockAuthBloc();
    });

    Future<void> pumpRegisterScreen(WidgetTester tester) async {
      await tester.pumpWidget(
        BlocProvider.value(
          value: mockAuthBloc,
          child: const MaterialApp(
            home: RegisterScreen(),
          ),
        ),
      );
    }

    testWidgets('harus menampilkan semua kolom input dan tombol daftar', (tester) async {
      whenListen(
        mockAuthBloc,
        Stream.fromIterable([AuthInitial()]),
        initialState: AuthInitial(),
      );

      await pumpRegisterScreen(tester);

      expect(find.byKey(const Key('ownerName_field')), findsOneWidget);
      expect(find.byKey(const Key('businessName_field')), findsOneWidget);
      expect(find.byKey(const Key('email_field')), findsOneWidget);
      expect(find.byKey(const Key('password_field')), findsOneWidget);
      
      // Menggunakan find.byKey yang lebih andal
      expect(find.byKey(const Key('register_button')), findsOneWidget);
    });
  });
}