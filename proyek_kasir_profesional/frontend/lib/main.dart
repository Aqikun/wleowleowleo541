// -- KODE UNTUK INTERAKSI LANJUTAN --
// -- FILE: lib/main.dart --

import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:frontend/src/core_app/routes/app_router.dart';
import 'package:frontend/src/shared/api/api_client.dart';

// Import untuk Authentication
import 'package:frontend/src/features/authentication/domain/auth_repository.dart';
import 'package:frontend/src/features/authentication/infrastructure/auth_repository_impl.dart';
import 'package:frontend/src/features/authentication/presentation/bloc/auth_bloc.dart';

// Import untuk Product
import 'package:frontend/src/features/retail/product/domain/product_repository.dart';
import 'package:frontend/src/features/retail/product/infrastructure/product_repository_impl.dart';
import 'package:frontend/src/features/retail/product/presentation/bloc/product_bloc.dart';

void main() {
  // // Setup semua dependensi di sini
  final ApiClient apiClient = ApiClient();
  final AuthRepository authRepository = AuthRepositoryImpl(apiClient);
  final ProductRepository productRepository = ProductRepositoryImpl(apiClient);

  runApp(MyApp(
    authRepository: authRepository,
    productRepository: productRepository,
  ));
}

class MyApp extends StatelessWidget {
  const MyApp({
    super.key,
    required this.authRepository,
    required this.productRepository,
  });

  final AuthRepository authRepository;
  final ProductRepository productRepository;

  @override
  Widget build(BuildContext context) {
    // // Gunakan MultiBlocProvider untuk mendaftarkan semua BLoC
    return MultiBlocProvider(
      providers: [
        BlocProvider<AuthBloc>(
          create: (context) => AuthBloc(authRepository: authRepository),
        ),
        BlocProvider<ProductBloc>(
          create: (context) => ProductBloc(productRepository),
        ),
        // // Nanti, BLoC lain bisa ditambahkan di sini
      ],
      child: MaterialApp(
        title: 'Aplikasi Kasir Profesional',
        theme: ThemeData(
          colorScheme: ColorScheme.fromSeed(seedColor: Colors.deepPurple),
          useMaterial3: true,
        ),
        debugShowCheckedModeBanner: false,
        onGenerateRoute: AppRouter.generateRoute,
        // === PERUBAHAN UTAMA DI SINI ===
        // Mengubah rute awal ke halaman login
        initialRoute: AppRouter.loginRoute, 
        // ==============================
      ),
    );
  }
}