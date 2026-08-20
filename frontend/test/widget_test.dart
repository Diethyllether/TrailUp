import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:trailup_app/main.dart';

void main() {
  testWidgets('TrailUp inicia na tela inicial', (WidgetTester tester) async {
    await tester.pumpWidget(const TrailUpApp());

    expect(find.byType(MaterialApp), findsOneWidget);
    expect(find.text('TrailUp'), findsOneWidget);
    expect(find.text('Criar conta'), findsOneWidget);
    expect(find.text('Já tenho conta'), findsOneWidget);
  });
}
