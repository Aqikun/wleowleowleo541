// test/features/authentication/login_screen_test.dart

import 'package:bloc_test/bloc_test.dart';
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:frontend/src/features/authentication/presentation/bloc/auth_bloc.dart';
import 'package:frontend/src/features/authentication/presentation/screens/login_screen.dart';

// Path import yang sudah diperbaiki
import '../../helpers/test_helpers.dart';

void main() {
  group('LoginScreen', () {
    late AuthBloc mockAuthBloc;

    setUp(() {
      mockAuthBloc = MockAuthBloc();
    });

    Future<void> pumpLoginScreen(WidgetTester tester) async {
      await tester.pumpWidget(
        BlocProvider.value(
          value: mockAuthBloc,
          child: const MaterialApp(
            home: LoginScreen(),
          ),
        ),
      );
    }

    testWidgets('harus menampilkan semua field dan tombol login', (tester) async {
      whenListen(
        mockAuthBloc,
        Stream.fromIterable([AuthInitial()]),
        initialState: AuthInitial(),
      );

      await pumpLoginScreen(tester);

      expect(find.byKey(const Key('login_email_field')), findsOneWidget);
      expect(find.byKey(const Key('login_password_field')), findsOneWidget);
      expect(find.widgetWithText(ElevatedButton, 'Login'), findsOneWidget);
    });
  });
}