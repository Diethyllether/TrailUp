import 'package:flutter/material.dart';

class AppColors {
  AppColors._();

  static const Color bgDark = Color(0xFF0F140F);
  static const Color bgMid = Color(0xFF1A211A);
  static const Color bgCard = Color(0xFF242E24);

  static const Color green = Color(0xFF2E8C47);
  static const Color greenLight = Color(0xFF3DB861);

  static const Color amber = Color(0xFFEB9E2E);
  static const Color red = Color(0xFFE63838);
  static const Color blueUser = Color(0xFF4D99FF);

  static const Color textPrimary = Color(0xFFF2F5EB);
  static const Color textDim = Color(0xFF8C9E8A);

  static Color difficultyColor(String? dificuldade) {
    switch (dificuldade?.toLowerCase()) {
      case 'fácil':
      case 'facil':
        return greenLight;
      case 'moderado':
      case 'moderada':
        return amber;
      case 'difícil':
      case 'dificil':
        return red;
      default:
        return textDim;
    }
  }
}

class AppTheme {
  AppTheme._();

  static ThemeData get dark {
    return ThemeData(
      brightness: Brightness.dark,
      scaffoldBackgroundColor: AppColors.bgDark,
      primaryColor: AppColors.green,
      splashColor: AppColors.green.withOpacity(0.2),
      colorScheme: const ColorScheme.dark(
        primary: AppColors.green,
        secondary: AppColors.amber,
        surface: AppColors.bgCard,
        error: AppColors.red,
      ),
      appBarTheme: const AppBarTheme(
        backgroundColor: Colors.transparent,
        elevation: 0,
        foregroundColor: AppColors.textPrimary,
        centerTitle: false,
      ),
      textTheme: const TextTheme(
        displayLarge: TextStyle(color: AppColors.textPrimary, fontWeight: FontWeight.bold, fontSize: 28),
        headlineMedium: TextStyle(color: AppColors.textPrimary, fontWeight: FontWeight.bold, fontSize: 22),
        titleMedium: TextStyle(color: AppColors.textPrimary, fontWeight: FontWeight.w600, fontSize: 16),
        bodyMedium: TextStyle(color: AppColors.textPrimary, fontSize: 14),
        bodySmall: TextStyle(color: AppColors.textDim, fontSize: 12),
      ),
      elevatedButtonTheme: ElevatedButtonThemeData(
        style: ElevatedButton.styleFrom(
          backgroundColor: AppColors.green,
          foregroundColor: Colors.white,
          disabledBackgroundColor: AppColors.green.withOpacity(0.4),
          padding: const EdgeInsets.symmetric(vertical: 16),
          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(14)),
          textStyle: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
        ),
      ),
      outlinedButtonTheme: OutlinedButtonThemeData(
        style: OutlinedButton.styleFrom(
          foregroundColor: AppColors.greenLight,
          padding: const EdgeInsets.symmetric(vertical: 16),
          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(14)),
        ),
      ),
      inputDecorationTheme: InputDecorationTheme(
        filled: true,
        fillColor: AppColors.bgCard,
        contentPadding: const EdgeInsets.symmetric(horizontal: 16, vertical: 14),
        border: OutlineInputBorder(
          borderRadius: BorderRadius.circular(14),
          borderSide: BorderSide.none,
        ),
        hintStyle: const TextStyle(color: AppColors.textDim),
      ),
      dividerColor: AppColors.bgCard,
    );
  }
}
