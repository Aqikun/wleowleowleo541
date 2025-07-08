// lib/src/features/retail/product/presentation/bloc/product_bloc.dart

import 'package:equatable/equatable.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:frontend/src/features/retail/product/domain/product_model.dart';
import 'package:frontend/src/features/retail/product/domain/product_repository.dart';

part 'product_event.dart';
part 'product_state.dart';

// ... (Isi kelas BLoC tidak berubah) ...
class ProductBloc extends Bloc<ProductEvent, ProductState> {
  final ProductRepository _productRepository;

  ProductBloc(this._productRepository) : super(ProductInitial()) {
    on<FetchAllProducts>(_onFetchAllProducts);
    on<AddProductRequested>(_onAddProductRequested);
    on<UpdateProductRequested>(_onUpdateProductRequested);
    on<DeleteProductRequested>(_onDeleteProductRequested);
  }

  Future<void> _onFetchAllProducts(
    FetchAllProducts event,
    Emitter<ProductState> emit,
  ) async {
    emit(ProductLoading());
    final result = await _productRepository.getAllProducts();
    result.fold(
      (failure) => emit(ProductFailure(failure.message)),
      (products) => emit(ProductDisplaySuccess(products)),
    );
  }

  Future<void> _onAddProductRequested(
    AddProductRequested event,
    Emitter<ProductState> emit,
  ) async {
    emit(ProductLoading());
    final result = await _productRepository.addProduct(
      name: event.name,
      description: event.description,
      price: event.price,
      stock: event.stock,
      category: event.category,
    );
    result.fold(
      (failure) => emit(ProductFailure(failure.message)),
      (product) => emit(const ProductActionSuccess('Produk berhasil ditambahkan')),
    );
  }

  Future<void> _onUpdateProductRequested(
    UpdateProductRequested event,
    Emitter<ProductState> emit,
  ) async {
    emit(ProductLoading());
    final result = await _productRepository.updateProduct(event.product);
    result.fold(
      (failure) => emit(ProductFailure(failure.message)),
      (product) => emit(const ProductActionSuccess('Produk berhasil diperbarui')),
    );
  }

  Future<void> _onDeleteProductRequested(
    DeleteProductRequested event,
    Emitter<ProductState> emit,
  ) async {
    emit(ProductLoading());
    final result = await _productRepository.deleteProduct(event.id);
    result.fold(
      (failure) => emit(ProductFailure(failure.message)),
      (_) => emit(const ProductActionSuccess('Produk berhasil dihapus')),
    );
  }
}