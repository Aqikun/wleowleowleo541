// lib/src/features/retail/product/presentation/bloc/product_event.dart

part of 'product_bloc.dart';

sealed class ProductEvent extends Equatable {
  const ProductEvent();

  @override
  List<Object> get props => [];
}

final class FetchAllProducts extends ProductEvent {}

final class AddProductRequested extends ProductEvent {
  final String name;
  final String description;
  final double price;
  final int stock;
  final String category;

  const AddProductRequested({
    required this.name,
    required this.description,
    required this.price,
    required this.stock,
    required this.category,
  });

  @override
  List<Object> get props => [name, description, price, stock, category];
}

final class UpdateProductRequested extends ProductEvent {
  final Product product; // // Ini akan otomatis merujuk ke model dari product_bloc.dart

  const UpdateProductRequested(this.product);

  @override
  List<Object> get props => [product];
}

final class DeleteProductRequested extends ProductEvent {
  final String id;

  const DeleteProductRequested(this.id);

  @override
  List<Object> get props => [id];
}