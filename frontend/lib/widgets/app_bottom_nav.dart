import 'package:flutter/material.dart';
import '../core/theme/app_theme.dart';

class AppBottomNav extends StatelessWidget {
  final int currentIndex;
  final ValueChanged<int> onTap;

  const AppBottomNav({super.key, required this.currentIndex, required this.onTap});

  static const _icons = [
    Icons.home_rounded,
    Icons.map_rounded,
    Icons.add_circle,
    Icons.favorite_rounded,
    Icons.person_rounded,
  ];
  static const _labels = ['Home', 'Mapa', '', 'Favoritos', 'Perfil'];

  @override
  Widget build(BuildContext context) {
    return Container(
      height: 64,
      color: AppColors.bgMid,
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceAround,
        children: List.generate(_icons.length, (i) {
          final selected = i == currentIndex;
          return GestureDetector(
            onTap: () => onTap(i),
            behavior: HitTestBehavior.opaque,
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Icon(
                  _icons[i],
                  color: selected ? AppColors.greenLight : AppColors.textDim,
                  size: i == 2 ? 30 : 22,
                ),
                if (_labels[i].isNotEmpty)
                  Text(
                    _labels[i],
                    style: TextStyle(
                      fontSize: 10,
                      color: selected ? AppColors.greenLight : AppColors.textDim,
                    ),
                  ),
              ],
            ),
          );
        }),
      ),
    );
  }
}
