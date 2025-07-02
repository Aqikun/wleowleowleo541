// # lib/main.dart

import 'package:flutter/material.dart';

// # Impor halaman login yang sudah kita buat
// # Ganti 'frontend' dengan nama proyek Anda jika berbeda
import 'package:frontend/src/features/authentication/presentation/screens/login_screen.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Aplikasi Kasir Profesional',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.deepPurple),
        useMaterial3: true,
      ),
      // # Di sini kita tentukan halaman pertama yang akan ditampilkan
      home: const LoginScreen(),
    );
  }
}