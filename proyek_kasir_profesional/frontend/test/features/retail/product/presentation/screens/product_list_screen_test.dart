// test/features/retail/product/presentation/screens/product_list_screen_test.dart

// test/features/retail/product/presentation/screens/product_list_screen_test.dart
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:bloc_test/bloc_test.dart';
import 'package:mocktail/mocktail.dart';

// Menggunakan import absolut
import 'package:frontend/src/features/retail/product/domain/product_model.dart';
import 'package:frontend/src/features/retail/product/presentation/bloc/product_bloc.dart';
import 'package:frontend/src/features/retail/product/presentation/screens/product_list_screen.dart';
import 'package:frontend/src/features/retail/product/presentation/widgets/product_card.dart';

// Helper tetap menggunakan import relatif
import '../../../../../helpers/test_helpers.dart';

void main() {
  late MockProductBloc mockProductBloc;

  Future<void> pumpWidget(WidgetTester tester) async {
    await tester.pumpWidget(
      MaterialApp(
        home: BlocProvider<ProductBloc>.value(
          value: mockProductBloc,
          child: const ProductListScreen(),
        ),
      ),
    );
  }

  setUp(() {
    mockProductBloc = MockProductBloc();
    // // Menambahkan fallback untuk event yang tidak kita duga dalam tes ini
    registerFallbackValue(FetchAllProducts());
  });

  tearDown(() {
    mockProductBloc.close();
  });

  final tProduct = Product(
    id: '1',
    name: 'Test Product',
    description: 'Test Description',
    price: 10000,
    stock: 10,
    category: 'Test',
  );

  testWidgets('mengirim FetchAllProducts event saat initState', (tester) async {
    whenListen(
      mockProductBloc,
      const Stream<ProductState>.empty(),
      initialState: ProductInitial(),
    );
    await pumpWidget(tester);
    verify(() => mockProductBloc.add(any(that: isA<FetchAllProducts>()))).called(1);
  });

  testWidgets('menampilkan CircularProgressIndicator saat state adalah loading',
      (tester) async {
    whenListen(
      mockProductBloc,
      Stream.fromIterable([ProductLoading()]),
      initialState: ProductInitial(),
    );
    await pumpWidget(tester);
    await tester.pump();
    expect(find.byType(CircularProgressIndicator), findsOneWidget);
  });

  testWidgets(
      'menampilkan ListView dengan ProductCard saat state adalah ProductDisplaySuccess dengan data',
      (tester) async {
    whenListen(
      mockProductBloc,
      Stream.fromIterable([ProductDisplaySuccess([tProduct])]),
      initialState: ProductInitial(),
    );
    await pumpWidget(tester);
    await tester.pumpAndSettle();
    expect(find.byType(ListView), findsOneWidget);
    expect(find.byType(ProductCard), findsOneWidget);
  });

  testWidgets(
      'menampilkan pesan "Belum ada produk" saat state adalah ProductDisplaySuccess tapi data kosong',
      (tester) async {
    whenListen(
      mockProductBloc,
      Stream.fromIterable([const ProductDisplaySuccess([])]),
      initialState: ProductInitial(),
    );
    await pumpWidget(tester);
    await tester.pumpAndSettle();
    expect(find.text('Belum ada produk. Silakan tambahkan.'), findsOneWidget);
  });

  testWidgets('menampilkan pesan error dan tombol Coba Lagi saat state adalah ProductFailure',
      (tester) async {
    whenListen(
      mockProductBloc,
      Stream.fromIterable([const ProductFailure('Server Error')]),
      initialState: ProductInitial(),
    );
    await pumpWidget(tester);
    await tester.pumpAndSettle();
    expect(find.text('Gagal memuat produk: Server Error'), findsOneWidget);
    expect(find.widgetWithText(ElevatedButton, 'Coba Lagi'), findsOneWidget);
  });
}