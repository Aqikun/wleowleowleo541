// lib/src/features/retail/product/presentation/screens/product_form_screen.dart

import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
// MENGGUNAKAN IMPORT ABSOLUT YANG BENAR
import 'package:frontend/src/features/retail/product/domain/product_model.dart';
import 'package:frontend/src/features/retail/product/presentation/bloc/product_bloc.dart';

class ProductFormScreen extends StatefulWidget {
  final Product? product;

  const ProductFormScreen({super.key, this.product});

  @override
  State<ProductFormScreen> createState() => _ProductFormScreenState();
}

class _ProductFormScreenState extends State<ProductFormScreen> {
  final _formKey = GlobalKey<FormState>();
  late TextEditingController _nameController;
  late TextEditingController _descriptionController;
  late TextEditingController _priceController;
  late TextEditingController _stockController;
  late TextEditingController _categoryController;

  bool get _isEditing => widget.product != null;

  @override
  void initState() {
    super.initState();
    _nameController = TextEditingController(text: widget.product?.name);
    _descriptionController =
        TextEditingController(text: widget.product?.description);
    _priceController =
        TextEditingController(text: widget.product?.price.toString());
    _stockController =
        TextEditingController(text: widget.product?.stock.toString());
    _categoryController = TextEditingController(text: widget.product?.category);
  }

  @override
  void dispose() {
    _nameController.dispose();
    _descriptionController.dispose();
    _priceController.dispose();
    _stockController.dispose();
    _categoryController.dispose();
    super.dispose();
  }

  void _submitForm() {
    if (_formKey.currentState!.validate()) {
      if (_isEditing) {
        final updatedProduct = Product(
          id: widget.product!.id,
          name: _nameController.text,
          description: _descriptionController.text,
          price: double.parse(_priceController.text),
          stock: int.parse(_stockController.text),
          category: _categoryController.text,
        );
        context.read<ProductBloc>().add(UpdateProductRequested(updatedProduct));
      } else {
        context.read<ProductBloc>().add(AddProductRequested(
              name: _nameController.text,
              description: _descriptionController.text,
              price: double.parse(_priceController.text),
              stock: int.parse(_stockController.text),
              category: _categoryController.text,
            ));
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(_isEditing ? 'Edit Produk' : 'Tambah Produk'),
      ),
      body: BlocListener<ProductBloc, ProductState>(
        listener: (context, state) {
          if (state is ProductActionSuccess) {
            Navigator.of(context).pop();
          }
        },
        child: Form(
          key: _formKey,
          child: SingleChildScrollView(
            padding: const EdgeInsets.all(16.0),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: [
                TextFormField(
                  controller: _nameController,
                  decoration: const InputDecoration(labelText: 'Nama Produk'),
                  validator: (value) {
                    if (value == null || value.isEmpty) {
                      return 'Nama produk tidak boleh kosong';
                    }
                    return null;
                  },
                ),
                const SizedBox(height: 16),
                TextFormField(
                  controller: _descriptionController,
                  decoration: const InputDecoration(labelText: 'Deskripsi'),
                  maxLines: 3,
                ),
                const SizedBox(height: 16),
                 TextFormField(
                  controller: _priceController,
                  decoration: const InputDecoration(labelText: 'Harga', prefixText: 'Rp '),
                  keyboardType: TextInputType.number,
                  inputFormatters: <TextInputFormatter>[
                    FilteringTextInputFormatter.digitsOnly
                  ],
                  validator: (value) {
                    if (value == null || value.isEmpty) {
                      return 'Harga tidak boleh kosong';
                    }
                    return null;
                  },
                ),
                const SizedBox(height: 16),
                TextFormField(
                  controller: _stockController,
                  decoration: const InputDecoration(labelText: 'Stok'),
                  keyboardType: TextInputType.number,
                   inputFormatters: <TextInputFormatter>[
                    FilteringTextInputFormatter.digitsOnly
                  ],
                  validator: (value) {
                    if (value == null || value.isEmpty) {
                      return 'Stok tidak boleh kosong';
                    }
                    return null;
                  },
                ),
                const SizedBox(height: 16),
                TextFormField(
                  controller: _categoryController,
                  decoration: const InputDecoration(labelText: 'Kategori'),
                   validator: (value) {
                    if (value == null || value.isEmpty) {
                      return 'Kategori tidak boleh kosong';
                    }
                    return null;
                  },
                ),
                const SizedBox(height: 32),
                ElevatedButton(
                  onPressed: _submitForm,
                  style: ElevatedButton.styleFrom(
                    padding: const EdgeInsets.symmetric(vertical: 16),
                  ),
                  child: const Text('Simpan Produk'),
                )
              ],
            ),
          ),
        ),
      ),
    );
  }
}