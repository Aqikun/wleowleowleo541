// lib/src/features/retail/product/domain/product_model.dart

import 'package:equatable/equatable.dart';

class Product extends Equatable {
  final String id;
  final String name;
  final String description;
  final double price;
  final int stock;
  final String category;

  const Product({
    required this.id,
    required this.name,
    required this.description,
    required this.price,
    required this.stock,
    required this.category,
  });

  @override
  List<Object?> get props => [id, name, description, price, stock, category];

  factory Product.fromJson(Map<String, dynamic> json) {
    return Product(
      id: (json['id'] ?? 0).toString(),
      name: json['name'] ?? '',
      description: json['description'] ?? '',
      
      // ===== PERBAIKAN FINAL DI SINI =====
      // Mengubah Teks harga menjadi Angka dengan aman
      price: double.tryParse(json['price']?.toString() ?? '0.0') ?? 0.0,
      // ===================================
      
      stock: json['stock'] as int? ?? 0,
      category: json['category'] ?? 'Uncategorized',
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'name': name,
      'description': description,
      // Saat mengirim ke backend, kita kirim sebagai angka
      'price': price, 
      'stock': stock,
      'category': category,
    };
  }
}