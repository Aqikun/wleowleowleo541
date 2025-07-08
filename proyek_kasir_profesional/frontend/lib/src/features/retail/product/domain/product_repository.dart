// lib/src/features/retail/product/domain/product_repository.dart
import 'package:fpdart/fpdart.dart';
import 'package:frontend/src/core_app/failures/failure.dart';
import 'package:frontend/src/features/retail/product/domain/product_model.dart';

abstract class ProductRepository {
  Future<Either<Failure, List<Product>>> getAllProducts();
  Future<Either<Failure, Product>> addProduct({
    required String name,
    required String description,
    required double price,
    required int stock,
    required String category,
  });
  Future<Either<Failure, Product>> updateProduct(Product product);
  Future<Either<Failure, void>> deleteProduct(String id);
}