// # /lib/src/features/authentication/presentation/screens/profile_screen.dart

import 'package:flutter/material.dart';

class ProfileScreen extends StatelessWidget {
  const ProfileScreen({super.key});

  @override
  Widget build(BuildContext context) {
    // # TODO: Data ini akan diambil dari state BLoC setelah login berhasil
    const String userName = 'Nama Pengguna';
    const String userEmail = 'email.pengguna@example.com';
    const String userRole = 'Owner';

    return Scaffold(
      appBar: AppBar(
        title: const Text('Profil Saya'),
        actions: [
          IconButton(
            icon: const Icon(Icons.logout),
            onPressed: () {
              // # TODO: Panggil BLoC untuk proses logout
              print('Logout button pressed');
            },
            tooltip: 'Logout',
          ),
        ],
      ),
      body: ListView(
        padding: const EdgeInsets.all(16.0),
        children: [
          const CircleAvatar(
            radius: 50,
            backgroundColor: Colors.deepPurple,
            child: Icon(Icons.person, size: 60, color: Colors.white),
          ),
          const SizedBox(height: 16),
          Text(
            userName,
            textAlign: TextAlign.center,
            style: Theme.of(context).textTheme.headlineSmall,
          ),
          Text(
            userRole,
            textAlign: TextAlign.center,
            style: Theme.of(context).textTheme.titleMedium?.copyWith(
                  color: Colors.grey.shade600,
                ),
          ),
          const SizedBox(height: 32),
          Card(
            child: ListTile(
              leading: const Icon(Icons.email, color: Colors.deepPurple),
              title: const Text('Email'),
              subtitle: const Text(userEmail),
            ),
          ),
          Card(
            child: ListTile(
              leading: const Icon(Icons.lock, color: Colors.deepPurple),
              title: const Text('Ganti Password'),
              trailing: const Icon(Icons.chevron_right),
              onTap: () {
                // # TODO: Navigasi ke halaman ganti password
                print('Navigate to change password page');
              },
            ),
          ),
          Card(
            child: ListTile(
              leading: const Icon(Icons.store, color: Colors.deepPurple),
              title: const Text('Informasi Toko'),
              trailing: const Icon(Icons.chevron_right),
              onTap: () {
                // # TODO: Navigasi ke halaman pengaturan toko
                print('Navigate to store settings page');
              },
            ),
          ),
        ],
      ),
    );
  }
}