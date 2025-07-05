// # lib/src/core_app/routes/app_router.dart
import 'package:flutter/material.dart';
import 'package:frontend/src/features/authentication/presentation/screens/forgot_password_screen.dart';
import 'package:frontend/src/features/authentication/presentation/screens/login_screen.dart';
import 'package:frontend/src/features/authentication/presentation/screens/register_screen.dart';

class AppRouter {
  static const String loginRoute = '/';
  static const String registerRoute = '/register';
  static const String forgotPasswordRoute = '/forgot-password';

  static Route<dynamic> generateRoute(RouteSettings settings) {
    switch (settings.name) {
      case loginRoute:
        return MaterialPageRoute(builder: (_) => const LoginScreen());
      case registerRoute:
        return MaterialPageRoute(builder: (_) => const RegisterScreen());
      case forgotPasswordRoute:
        return MaterialPageRoute(builder: (_) => const ForgotPasswordScreen());
      default:
        return MaterialPageRoute(
            builder: (_) => Scaffold(
                  body: Center(
                      child: Text('No route defined for ${settings.name}')),
                ));
    }
  }
}