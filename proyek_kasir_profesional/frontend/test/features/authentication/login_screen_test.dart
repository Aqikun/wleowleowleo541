// # test/features/authentication/login_screen_test.dart

import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';

// # Ganti 'frontend' dengan nama proyek Anda jika berbeda
import 'package:frontend/src/features/authentication/presentation/screens/login_screen.dart'; 

void main() {
  // # Grupkan semua tes yang berhubungan dengan LoginScreen
  group('LoginScreen Widget Test', () {
    // # Tes 1: Memastikan semua widget awal tampil dengan benar
    testWidgets('menampilkan semua field dan tombol saat pertama kali dibuka',
        (WidgetTester tester) async {
      // # Bangun widget LoginScreen di lingkungan tes
      await tester.pumpWidget(const MaterialApp(home: LoginScreen()));

      // # Cari widget berdasarkan teks atau ikon
      expect(find.text('Login'), findsWidgets); // Judul AppBar dan Tombol
      expect(find.text('Email'), findsOneWidget);
      expect(find.text('Password'), findsOneWidget);
      expect(find.text('Lupa Password?'), findsOneWidget);
      expect(find.byIcon(Icons.store), findsOneWidget);
    });

    // # Tes 2: Memastikan validator email berfungsi
    testWidgets(
        'menampilkan pesan error ketika email kosong dan tombol login ditekan',
        (WidgetTester tester) async {
      await tester.pumpWidget(const MaterialApp(home: LoginScreen()));

      // # Temukan tombol login dan tekan
      await tester.tap(find.byType(ElevatedButton));

      // # "Rebuild" widget setelah menekan tombol untuk menampilkan pesan error
      await tester.pump();

      // # Harapkan ada pesan error yang muncul
      expect(find.text('Email tidak boleh kosong'), findsOneWidget);
    });

    // # Tes 3: Memastikan validator email untuk format yang salah
    testWidgets(
        'menampilkan pesan error ketika format email salah',
        (WidgetTester tester) async {
      await tester.pumpWidget(const MaterialApp(home: LoginScreen()));

      // # Masukkan teks yang bukan email ke dalam field email
      await tester.enterText(find.byType(TextFormField).first, 'bukanemail');
      
      // # Tekan tombol login
      await tester.tap(find.byType(ElevatedButton));
      await tester.pump(); // Rebuild

      // # Harapkan ada pesan error format
      expect(find.text('Masukkan email yang valid'), findsOneWidget);
    });

    // # Tes 4: Memastikan validator password berfungsi
    testWidgets(
        'menampilkan pesan error ketika password kosong dan email sudah diisi',
        (WidgetTester tester) async {
      await tester.pumpWidget(const MaterialApp(home: LoginScreen()));

      // # Isi email dengan benar
      await tester.enterText(find.byType(TextFormField).first, 'test@test.com');
      
      // # Tekan tombol login (password sengaja dikosongkan)
      await tester.tap(find.byType(ElevatedButton));
      await tester.pump(); // Rebuild

      // # Harapkan pesan error untuk password
      expect(find.text('Password tidak boleh kosong'), findsOneWidget);
      // # Pastikan pesan error email tidak muncul
      expect(find.text('Email tidak boleh kosong'), findsNothing);
    });
  });
}