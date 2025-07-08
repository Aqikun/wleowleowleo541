// lib/src/features/retail/product/presentation/bloc/product_state.dart

part of 'product_bloc.dart';

sealed class ProductState extends Equatable {
  const ProductState();

  @override
  List<Object> get props => [];
}

final class ProductInitial extends ProductState {}

final class ProductLoading extends ProductState {}

final class ProductDisplaySuccess extends ProductState {
  final List<Product> products; // // Ini juga akan merujuk ke model yang benar

  const ProductDisplaySuccess(this.products);

  @override
  List<Object> get props => [products];
}

final class ProductActionSuccess extends ProductState {
  final String message;

  const ProductActionSuccess(this.message);

  @override
  List<Object> get props => [message];
}

final class ProductFailure extends ProductState {
  final String message;

  const ProductFailure(this.message);

  @override
  List<Object> get props => [message];
}