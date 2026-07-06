import 'package:flutter/material.dart';
import '../core/theme/app_theme.dart';

class DifficultyBadge extends StatelessWidget {
  final String? dificuldade;
  const DifficultyBadge({super.key, required this.dificuldade});

  static String _rotulo(String? codigo) {
    switch (codigo?.toLowerCase()) {
      case 'facil':
      case 'fácil':
        return 'Fácil';
      case 'moderada':
      case 'moderado':
        return 'Moderado';
      case 'dificil':
      case 'difícil':
        return 'Difícil';
      default:
        return codigo ?? '—';
    }
  }

  @override
  Widget build(BuildContext context) {
    final color = AppColors.difficultyColor(dificuldade);
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
      decoration: BoxDecoration(
        color: color.withOpacity(0.9),
        borderRadius: BorderRadius.circular(14),
      ),
      child: Text(
        _rotulo(dificuldade),
        style: const TextStyle(fontSize: 11, fontWeight: FontWeight.bold, color: Colors.black87),
      ),
    );
  }
}
