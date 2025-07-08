// lib/src/features/retail/product/presentation/screens/product_list_screen.dart

import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:frontend/src/features/retail/product/presentation/bloc/product_bloc.dart'; // GANTI NAMA PAKET
import 'package:frontend/src/features/retail/product/presentation/screens/product_form_screen.dart'; // GANTI NAMA PAKET
import 'package:frontend/src/features/retail/product/presentation/widgets/product_card.dart'; // GANTI NAMA PAKET

class ProductListScreen extends StatefulWidget {
  const ProductListScreen({super.key});

  @override
  State<ProductListScreen> createState() => _ProductListScreenState();
}

class _ProductListScreenState extends State<ProductListScreen> {
  @override
  void initState() {
    super.initState();
    context.read<ProductBloc>().add(FetchAllProducts());
  }

  void _showDeleteConfirmation(BuildContext context, String productId) {
    showDialog(
      context: context,
      builder: (BuildContext dialogContext) {
        return AlertDialog(
          title: const Text('Hapus Produk'),
          content: const Text('Apakah Anda yakin ingin menghapus produk ini?'),
          actions: <Widget>[
            TextButton(
              child: const Text('Batal'),
              onPressed: () {
                Navigator.of(dialogContext).pop();
              },
            ),
            TextButton(
              child: const Text('Hapus', style: TextStyle(color: Colors.red)),
              onPressed: () {
                context.read<ProductBloc>().add(DeleteProductRequested(productId));
                Navigator.of(dialogContext).pop();
              },
            ),
          ],
        );
      },
    );
  }


  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Manajemen Produk'),
        actions: [
          IconButton(
            icon: const Icon(Icons.add_circle_outline),
            tooltip: 'Tambah Produk',
            onPressed: () {
              // // Navigasi ke form tambah produk (tanpa mengirim data produk)
              Navigator.of(context).push(
                MaterialPageRoute(builder: (_) => const ProductFormScreen()),
              );
            },
          ),
        ],
      ),
      body: BlocConsumer<ProductBloc, ProductState>(
        listener: (context, state) {
          if (state is ProductActionSuccess) {
            ScaffoldMessenger.of(context).showSnackBar(
              SnackBar(
                content: Text(state.message),
                backgroundColor: Colors.green,
              ),
            );
            context.read<ProductBloc>().add(FetchAllProducts());
          }
          if (state is ProductFailure) {
             ScaffoldMessenger.of(context).showSnackBar(
              SnackBar(
                content: Text(state.message),
                backgroundColor: Colors.red,
              ),
            );
          }
        },
        builder: (context, state) {
          // // Logika ini sedikit disesuaikan agar loading tidak menimpa data yang ada
          final currentState = context.watch<ProductBloc>().state;
          if (currentState is ProductLoading && currentState is! ProductDisplaySuccess) {
            return const Center(child: CircularProgressIndicator());
          }

          if (currentState is ProductDisplaySuccess) {
            if (currentState.products.isEmpty) {
              return const Center(
                child: Text('Belum ada produk. Silakan tambahkan.'),
              );
            }
            
            return ListView.builder(
              itemCount: currentState.products.length,
              itemBuilder: (context, index) {
                final product = currentState.products[index];
                return ProductCard(
                  product: product,
                  onEdit: () {
                    // // Navigasi ke form edit (dengan mengirim data produk)
                    Navigator.of(context).push(
                      MaterialPageRoute(
                        builder: (_) => ProductFormScreen(product: product),
                      ),
                    );
                  },
                  onDelete: () {
                    _showDeleteConfirmation(context, product.id);
                  },
                );
              },
            );
          }
          if (currentState is ProductFailure && currentState is! ProductActionSuccess) {
             return Center(
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Text(
                    'Gagal memuat produk: ${currentState.message}',
                    style: const TextStyle(color: Colors.red),
                  ),
                  const SizedBox(height: 10),
                  ElevatedButton(onPressed: (){
                     context.read<ProductBloc>().add(FetchAllProducts());
                  }, child: const Text('Coba Lagi'))
                ],
              ),
            );
          }

          // // Fallback untuk state awal atau tak terduga
          return const Center(child: CircularProgressIndicator());
        },
      ),
    );
  }
}