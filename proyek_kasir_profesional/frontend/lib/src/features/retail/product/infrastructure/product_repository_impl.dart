// lib/src/features/retail/product/infrastructure/product_repository_impl.dart

import 'package:fpdart/fpdart.dart';
import 'package:frontend/src/core_app/failures/failure.dart';
import 'package:frontend/src/shared/api/api_client.dart';
import 'package:frontend/src/features/retail/product/domain/product_model.dart';
import 'package:frontend/src/features/retail/product/domain/product_repository.dart';

class ProductRepositoryImpl implements ProductRepository {
  final ApiClient apiClient;

  ProductRepositoryImpl(this.apiClient);

  @override
  Future<Either<Failure, Product>> addProduct({
    required String name,
    required String description,
    required double price,
    required int stock,
    required String category,
  }) async {
    try {
      final response = await apiClient.post(
        '/products',
        data: {
          'name': name,
          'description': description,
          'price': price,
          'stock': stock,
          'category': category,
        },
      );
      // PERBAIKAN: Gunakan response.data bukan response['data']
      return Right(Product.fromJson(response.data));
    } catch (e) {
      return Left(Failure(e.toString()));
    }
  }

  @override
  Future<Either<Failure, void>> deleteProduct(String id) async {
    try {
      // PERBAIKAN: Panggil metode .delete() yang sudah kita buat
      await apiClient.delete('/products/$id');
      return const Right(null);
    } catch (e) {
      return Left(Failure(e.toString()));
    }
  }

  @override
  Future<Either<Failure, List<Product>>> getAllProducts() async {
    try {
      final response = await apiClient.get('/products');
      // PERBAIKAN: Gunakan response.data bukan response['data']
      final products = (response.data as List)
          .map((productJson) => Product.fromJson(productJson))
          .toList();
      return Right(products);
    } catch (e) {
      return Left(Failure(e.toString()));
    }
  }

  @override
  Future<Either<Failure, Product>> updateProduct(Product product) async {
    try {
      // PERBAIKAN: Panggil metode .put() yang sudah kita buat
      final response = await apiClient.put(
        '/products/${product.id}',
        data: product.toJson(),
      );
      // PERBAIKAN: Gunakan response.data bukan response['data']
      return Right(Product.fromJson(response.data));
    } catch (e) {
      return Left(Failure(e.toString()));
    }
  }
}