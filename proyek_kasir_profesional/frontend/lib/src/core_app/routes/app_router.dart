// -- KODE UNTUK INTERAKSI LANJUTAN --
// -- FILE: lib/src/core_app/routes/app_router.dart --

import 'package:flutter/material.dart';

// Import untuk Authentication
import 'package:frontend/src/features/authentication/presentation/screens/forgot_password_screen.dart';
import 'package:frontend/src/features/authentication/presentation/screens/login_screen.dart';
import 'package:frontend/src/features/authentication/presentation/screens/register_screen.dart';

// Import untuk Product
import 'package:frontend/src/features/retail/product/presentation/screens/product_list_screen.dart';

// === TAMBAHAN BARU ===
// Import untuk Home
import 'package:frontend/src/features/home/presentation/screens/home_screen.dart';
// =====================

class AppRouter {
  // Rute Otentikasi
  static const String loginRoute = '/';
  static const String registerRoute = '/register';
  static const String forgotPasswordRoute = '/forgot-password';

  // Rute Produk
  static const String productListRoute = '/products';

  // === TAMBAHAN BARU ===
  // Rute Home
  static const String homeRoute = '/home';
  // =====================


  static Route<dynamic> generateRoute(RouteSettings settings) {
    switch (settings.name) {
      // Rute Otentikasi
      case loginRoute:
        return MaterialPageRoute(builder: (_) => const LoginScreen());
      case registerRoute:
        return MaterialPageRoute(builder: (_) => const RegisterScreen());
      case forgotPasswordRoute:
        return MaterialPageRoute(builder: (_) => const ForgotPasswordScreen());

      // Rute Produk
      case productListRoute:
        return MaterialPageRoute(builder: (_) => const ProductListScreen());

      // === TAMBAHAN BARU ===
      case homeRoute:
        return MaterialPageRoute(builder: (_) => const HomeScreen());
      // =====================

      default:
        return MaterialPageRoute(
            builder: (_) => Scaffold(
                  body: Center(
                      child: Text('No route defined for ${settings.name}')),
                ));
    }
  }
}