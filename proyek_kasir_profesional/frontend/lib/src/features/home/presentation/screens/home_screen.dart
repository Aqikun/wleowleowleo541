// -- KODE UNTUK INTERAKSI LANJUTAN --
// -- FILE: lib/src/features/home/presentation/screens/home_screen.dart --

import 'package:flutter/material.dart';
// === PENAMBAHAN BARU ===
import 'package:frontend/src/core_app/routes/app_router.dart';
// =========================

class HomeScreen extends StatelessWidget {
  const HomeScreen({super.key});

  // Nama rute untuk navigasi yang mudah
  static const String routeName = '/home';

  @override
  Widget build(BuildContext context) {
    // Dummy data untuk desain awal
    const String userName = "Budi Susanto";
    const String userRole = "Owner";
    const String currentBranch = "Toko Cabang Padang";

    return Scaffold(
      appBar: AppBar(
        // Menghilangkan tombol kembali otomatis
        automaticallyImplyLeading: false, 
        leading: const Padding(
          padding: EdgeInsets.all(8.0),
          // Placeholder untuk foto profil
          child: CircleAvatar(
            backgroundColor: Colors.blueAccent,
            child: Icon(Icons.person, color: Colors.white),
          ),
        ),
        title: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text(
              'Selamat datang,',
              style: TextStyle(fontSize: 14),
            ),
            Text(
              userName,
              style: const TextStyle(
                fontSize: 18,
                fontWeight: FontWeight.bold,
              ),
            ),
          ],
        ),
        // Placeholder untuk menu dropdown cabang, notifikasi, dan logout
        actions: [
          // Nanti di sini kita tambahkan dropdown cabang jika user adalah Owner/Admin Global
          IconButton(
            icon: const Icon(Icons.notifications_none),
            onPressed: () {
              // TODO: Implementasi Pusat Notifikasi
            },
          ),
          IconButton(
            icon: const Icon(Icons.logout),
            onPressed: () {
              // TODO: Implementasi fungsi Logout
              // Ini akan memanggil AuthBloc.add(LogoutRequested())
            },
          ),
        ],
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Header untuk bagian navigasi utama
            const Text(
              'Dasbor Utama',
              style: TextStyle(fontSize: 22, fontWeight: FontWeight.bold),
            ),
            Text(
              'Peran: $userRole di $currentBranch',
              style: TextStyle(fontSize: 16, color: Colors.grey[700]),
            ),
            const SizedBox(height: 20),

            // GridView untuk kartu-kartu navigasi
            GridView.count(
              crossAxisCount: 2, // 2 kartu per baris
              crossAxisSpacing: 16,
              mainAxisSpacing: 16,
              shrinkWrap: true, // Agar GridView tidak error di dalam Column
              physics: const NeverScrollableScrollPhysics(), // Agar tidak bisa di-scroll terpisah
              children: [ // Dihapus 'const' agar onTap bisa berfungsi
                // Placeholder untuk kartu-kartu yang kita diskusikan
                // Nantinya ini akan dibangun secara dinamis dari BLoC
                _NavigationCard(
                  title: 'Sesi Kasir',
                  icon: Icons.point_of_sale,
                  color: Colors.green,
                  isLocked: false,
                  onTap: () {
                    // TODO: Navigasi ke halaman kasir
                  },
                ),
                // === PERUBAHAN UTAMA DI SINI ===
                _NavigationCard(
                  title: 'Manajemen Produk',
                  icon: Icons.inventory_2,
                  color: Colors.blue,
                  isLocked: false,
                  onTap: () {
                    Navigator.pushNamed(context, AppRouter.productListRoute);
                  },
                ),
                // ==============================
                _NavigationCard(
                  title: 'Laporan Penjualan',
                  icon: Icons.bar_chart,
                  color: Colors.orange,
                  isLocked: false,
                   onTap: () {
                    // TODO: Navigasi ke halaman laporan
                  },
                ),
                const _NavigationCard(
                  title: 'Manajemen Tim',
                  icon: Icons.group,
                  color: Colors.purple,
                  isLocked: true, // Contoh kartu terkunci
                  // onTap tidak perlu karena terkunci
                ),
              ],
            ),
             const SizedBox(height: 30),
            
            // Placeholder untuk bagian Upselling khusus Owner
            const Text(
              'Tingkatkan Potensi Bisnis',
              style: TextStyle(fontSize: 22, fontWeight: FontWeight.bold),
            ),
             const SizedBox(height: 10),
            const _UpsellCard(
              title: "Manajemen Multi-Cabang",
              description: "Kelola semua cabang Anda dari satu dasbor.",
            )

          ],
        ),
      ),
    );
  }
}

// Widget private untuk kartu navigasi agar kode lebih rapi
class _NavigationCard extends StatelessWidget {
  final String title;
  final IconData icon;
  final Color color;
  final bool isLocked;
  final VoidCallback? onTap; // Mengubah menjadi nullable

  const _NavigationCard({
    required this.title,
    required this.icon,
    required this.color,
    this.isLocked = false,
    this.onTap, // Mengubah menjadi opsional
  });

  @override
  Widget build(BuildContext context) {
    return Card(
      elevation: 4,
      color: isLocked ? Colors.grey[300] : Colors.white,
      child: InkWell(
        // Menggunakan onTap yang sudah didefinisikan
        onTap: isLocked ? null : onTap,
        child: Stack(
          children: [
            Center(
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: <Widget>[
                  Icon(icon, size: 48.0, color: isLocked ? Colors.grey[600] : color),
                  const SizedBox(height: 10),
                  Text(
                    title,
                    textAlign: TextAlign.center,
                    style: TextStyle(
                      fontSize: 16.0,
                      fontWeight: FontWeight.bold,
                      color: isLocked ? Colors.grey[600] : Colors.black87,
                    ),
                  ),
                ],
              ),
            ),
            if (isLocked)
              Container(
                alignment: Alignment.topRight,
                padding: const EdgeInsets.all(8.0),
                child: Icon(Icons.lock, color: Colors.grey[800]),
              ),
          ],
        ),
      ),
    );
  }
}


// Widget private untuk kartu upselling
class _UpsellCard extends StatelessWidget {
    final String title;
    final String description;

  const _UpsellCard({required this.title, required this.description});

  @override
  Widget build(BuildContext context) {
    return Card(
      color: Colors.blueGrey[50],
      child: ListTile(
        leading: Icon(Icons.lock_outline, color: Colors.blueGrey[600]),
        title: Text(title, style: const TextStyle(fontWeight: FontWeight.bold)),
        subtitle: Text(description),
        trailing: ElevatedButton(
          child: const Text('Upgrade'),
          onPressed: () {
            // TODO: Arahkan ke halaman langganan
          },
        ),
      ),
    );
  }
}