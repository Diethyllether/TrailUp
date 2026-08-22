import 'package:flutter/material.dart';
import '../core/theme/app_theme.dart';
import '../models/trilha.dart';
import 'difficulty_badge.dart';

class TrilhaCard extends StatelessWidget {
  final Trilha trilha;
  final VoidCallback? onTap;
  final VoidCallback? onFavoritar;

  const TrilhaCard({super.key, required this.trilha, this.onTap, this.onFavoritar});

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: onTap,
      child: Container(
        width: 190,
        decoration: BoxDecoration(color: AppColors.bgCard, borderRadius: BorderRadius.circular(16)),
        clipBehavior: Clip.antiAlias,
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Stack(
              children: [
                Container(
                  height: 110,
                  width: double.infinity,
                  color: AppColors.bgMid,
                  child: trilha.imagemCapa != null
                      ? Image.network(trilha.imagemCapa!, fit: BoxFit.cover)
                      : const Center(child: Icon(Icons.terrain, color: AppColors.textDim, size: 32)),
                ),
                Positioned(top: 10, left: 10, child: DifficultyBadge(dificuldade: trilha.dificuldade)),
                if (onFavoritar != null)
                  Positioned(
                    top: 8,
                    right: 8,
                    child: GestureDetector(
                      onTap: onFavoritar,
                      child: CircleAvatar(
                        radius: 15,
                        backgroundColor: Colors.black.withOpacity(0.45),
                        child: const Icon(Icons.favorite_border, size: 15, color: Colors.white),
                      ),
                    ),
                  ),
              ],
            ),
            Padding(
              padding: const EdgeInsets.all(12),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    trilha.nome,
                    maxLines: 1,
                    overflow: TextOverflow.ellipsis,
                    style: const TextStyle(
                        color: AppColors.textPrimary, fontWeight: FontWeight.bold, fontSize: 14),
                  ),
                  const SizedBox(height: 4),
                  if (trilha.localizacao != null && trilha.localizacao!.isNotEmpty)
                    Text(
                      trilha.localizacao!,
                      maxLines: 1,
                      overflow: TextOverflow.ellipsis,
                      style: const TextStyle(color: AppColors.textDim, fontSize: 10),
                    ),
                  Text(
                    '📍 ${trilha.distancia?.toStringAsFixed(1) ?? '--'} km  ⏱ ${trilha.tempoEstimadoFormatado}',
                    style: const TextStyle(color: AppColors.textDim, fontSize: 11),
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}
