// # lib/main.dart

import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:frontend/src/core_app/routes/app_router.dart'; // <-- Impor router baru kita
import 'package:frontend/src/shared/api/api_client.dart';
import 'package:frontend/src/features/authentication/domain/auth_repository.dart';
import 'package:frontend/src/features/authentication/infrastructure/auth_repository_impl.dart';
import 'package:frontend/src/features/authentication/presentation/bloc/auth_bloc.dart';

void main() {
  final ApiClient apiClient = ApiClient();
  final AuthRepository authRepository = AuthRepositoryImpl(apiClient);
  runApp(MyApp(authRepository: authRepository));
}

class MyApp extends StatelessWidget {
  const MyApp({super.key, required this.authRepository});
  final AuthRepository authRepository;

  @override
  Widget build(BuildContext context) {
    return BlocProvider(
      create: (context) => AuthBloc(authRepository: authRepository),
      child: MaterialApp(
        title: 'Aplikasi Kasir Profesional',
        theme: ThemeData(
          colorScheme: ColorScheme.fromSeed(seedColor: Colors.deepPurple),
          useMaterial3: true,
        ),
        debugShowCheckedModeBanner: false,
        
        // # BARIS-BARIS YANG DIPERBARUI
        onGenerateRoute: AppRouter.generateRoute,
        initialRoute: AppRouter.loginRoute,
      ),
    );
  }
}