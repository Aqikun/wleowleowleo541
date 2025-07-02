// # /lib/src/features/authentication/presentation/screens/login_screen.dart

import 'package:flutter/material.dart';

class LoginScreen extends StatefulWidget {
  const LoginScreen({super.key});

  @override
  State<LoginScreen> createState() => _LoginScreenState();
}

class _LoginScreenState extends State<LoginScreen> {
  // # Controller untuk mengambil input dari text field
  final _emailController = TextEditingController();
  final _passwordController = TextEditingController();
  final _formKey = GlobalKey<FormState>(); // # Kunci untuk validasi form

  @override
  void dispose() {
    // # Selalu dispose controller untuk menghindari memory leak
    _emailController.dispose();
    _passwordController.dispose();
    super.dispose();
  }

  void _login() {
    // # Cek apakah semua input valid
    if (_formKey.currentState!.validate()) {
      // # Jika valid, ambil data dari controller
      final email = _emailController.text;
      final password = _passwordController.text;

      // # TODO: Panggil BLoC/Cubit untuk mengirim data ke API Backend
      print('Login attempt with Email: $email, Password: $password');

      // # Di sini kita akan menambahkan logika untuk menampilkan loading
      // # dan menangani respons dari server (sukses atau gagal)
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Login'),
      ),
      body: Center(
        child: SingleChildScrollView(
          padding: const EdgeInsets.all(24.0),
          child: Form(
            key: _formKey,
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: [
                // # Anggap ini adalah logo aplikasi kita
                const Icon(Icons.store, size: 80, color: Colors.deepPurple),
                const SizedBox(height: 40),

                // # Text Field untuk Email
                TextFormField(
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
                    if (!value.contains('@')) {
                      return 'Masukkan email yang valid';
                    }
                    return null;
                  },
                ),
                const SizedBox(height: 16),

                // # Text Field untuk Password
                TextFormField(
                  controller: _passwordController,
                  decoration: const InputDecoration(
                    labelText: 'Password',
                    border: OutlineInputBorder(),
                    prefixIcon: Icon(Icons.lock),
                  ),
                  obscureText: true, // # Menyembunyikan teks password
                  validator: (value) {
                    if (value == null || value.isEmpty) {
                      return 'Password tidak boleh kosong';
                    }
                    return null;
                  },
                ),
                const SizedBox(height: 8),

                // # Tombol Lupa Password
                Align(
                  alignment: Alignment.centerRight,
                  child: TextButton(
                    onPressed: () {
                      // # TODO: Navigasi ke halaman Lupa Password
                      print('Navigasi ke halaman Lupa Password');
                    },
                    child: const Text('Lupa Password?'),
                  ),
                ),
                const SizedBox(height: 24),

                // # Tombol Login Utama
                ElevatedButton(
                  onPressed: _login,
                  style: ElevatedButton.styleFrom(
                    padding: const EdgeInsets.symmetric(vertical: 16),
                    backgroundColor: Colors.deepPurple,
                    foregroundColor: Colors.white,
                  ),
                  child: const Text('LOGIN'),
                ),
                const SizedBox(height: 16),

                // # Tombol untuk ke Halaman Registrasi
                Row(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    const Text('Belum punya akun?'),
                    TextButton(
                      onPressed: () {
                        // # TODO: Navigasi ke halaman Registrasi
                        print('Navigasi ke halaman Registrasi');
                      },
                      child: const Text('Daftar di sini'),
                    ),
                  ],
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}