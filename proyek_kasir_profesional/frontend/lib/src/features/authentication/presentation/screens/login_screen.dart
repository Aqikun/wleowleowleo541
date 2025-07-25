// -- KODE UNTUK INTERAKSI LANJUTAN --
// -- FILE: lib/src/features/authentication/presentation/screens/login_screen.dart --

import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:frontend/src/core_app/routes/app_router.dart';
import 'package:frontend/src/features/authentication/presentation/bloc/auth_bloc.dart';

class LoginScreen extends StatelessWidget {
  const LoginScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Center(
        child: SingleChildScrollView(
          child: Padding(
            padding: const EdgeInsets.all(24.0),
            // === PERUBAHAN UTAMA: Menambahkan BlocListener ===
            child: BlocListener<AuthBloc, AuthState>(
              listener: (context, state) {
                // Dengarkan HANYA state AuthLoginSuccess
                if (state is AuthLoginSuccess) {
                  // Tampilkan pesan sukses sebentar
                  ScaffoldMessenger.of(context)
                    ..hideCurrentSnackBar()
                    ..showSnackBar(
                      const SnackBar(
                        content: Text('Login Berhasil!'),
                        backgroundColor: Colors.green,
                      ),
                    );
                  // Navigasi ke HomeScreen dan hapus semua rute sebelumnya
                  Navigator.pushNamedAndRemoveUntil(
                    context,
                    AppRouter.homeRoute,
                    (route) => false, // Predikat ini menghapus semua rute
                  );
                }
                // Tampilkan pesan error jika login gagal
                if (state is AuthFailure) {
                   ScaffoldMessenger.of(context)
                    ..hideCurrentSnackBar()
                    ..showSnackBar(
                      SnackBar(
                        content: Text('Login Gagal: ${state.message}'),
                        backgroundColor: Colors.red,
                      ),
                    );
                }
              },
              child: const LoginForm(),
            ),
            // ============================================
          ),
        ),
      ),
    );
  }
}

class LoginForm extends StatefulWidget {
  const LoginForm({super.key});

  @override
  State<LoginForm> createState() => _LoginFormState();
}

class _LoginFormState extends State<LoginForm> {
  final _formKey = GlobalKey<FormState>();
  final _emailController = TextEditingController();
  final _passwordController = TextEditingController();

  @override
  void dispose() {
    _emailController.dispose();
    _passwordController.dispose();
    super.dispose();
  }

  void _onLoginPressed() {
    if (_formKey.currentState!.validate()) {
      context.read<AuthBloc>().add(
            LoginButtonPressed(
              email: _emailController.text,
              password: _passwordController.text,
            ),
          );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Form(
      key: _formKey,
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          const Icon(Icons.lock_outline, size: 80, color: Colors.blueAccent),
          const SizedBox(height: 8),
          const Text(
            'Selamat Datang',
            textAlign: TextAlign.center,
            style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
          ),
          const SizedBox(height: 24),
          TextFormField(
            key: const Key('login_email_field'),
            controller: _emailController,
            decoration: const InputDecoration(
              labelText: 'Email',
              border: OutlineInputBorder(),
              prefixIcon: Icon(Icons.email),
            ),
            keyboardType: TextInputType.emailAddress,
            validator: (value) {
              if (value == null || value.isEmpty) {
                return 'Email tidak boleh kosong';
              }
              return null;
            },
          ),
          const SizedBox(height: 16),
          TextFormField(
            key: const Key('login_password_field'),
            controller: _passwordController,
            decoration: const InputDecoration(
              labelText: 'Password',
              border: OutlineInputBorder(),
              prefixIcon: Icon(Icons.lock),
            ),
            obscureText: true,
            validator: (value) {
              if (value == null || value.isEmpty) {
                return 'Password tidak boleh kosong';
              }
              return null;
            },
          ),
          const SizedBox(height: 24),
          // BlocBuilder sekarang hanya fokus pada status loading
          BlocBuilder<AuthBloc, AuthState>(
            buildWhen: (previous, current) => current is AuthLoading || previous is AuthLoading,
            builder: (context, state) {
              if (state is AuthLoading) {
                return const Center(child: CircularProgressIndicator());
              }
              return ElevatedButton(
                key: const Key('login_button'),
                onPressed: _onLoginPressed,
                style: ElevatedButton.styleFrom(
                  padding: const EdgeInsets.symmetric(vertical: 16),
                ),
                child: const Text('LOGIN', style: TextStyle(fontSize: 16)),
              );
            },
          ),
          const SizedBox(height: 16),
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              TextButton(
                onPressed: () {
                  // Menggunakan AppRouter untuk navigasi
                  Navigator.pushNamed(context, AppRouter.forgotPasswordRoute);
                },
                child: const Text('Lupa Password?'),
              ),
              TextButton(
                onPressed: () {
                  // Menggunakan AppRouter untuk navigasi
                  Navigator.pushNamed(context, AppRouter.registerRoute);
                },
                child: const Text('Buat Akun'),
              ),
            ],
          ),
        ],
      ),
    );
  }
}