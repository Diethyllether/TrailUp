import 'package:flutter/material.dart';
import 'core/theme/app_theme.dart';
import 'screens/splash/splash_screen.dart';

void main() {
  runApp(const TrailUpApp());
}

class TrailUpApp extends StatelessWidget {
  const TrailUpApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'TrailUp',
      debugShowCheckedModeBanner: false,
      theme: AppTheme.dark,
      home: const SplashScreen(),
    );
  }
}
