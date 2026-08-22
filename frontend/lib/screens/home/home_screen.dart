import 'package:flutter/material.dart';
import '../../core/theme/app_theme.dart';
import '../../models/usuario.dart';
import '../../widgets/app_bottom_nav.dart';
import '../../widgets/criar_evento_sheet.dart';
import '../map/map_screen.dart';
import '../profile/profile_screen.dart';
import 'favoritos_tab.dart';
import 'home_tab.dart';

class HomeScreen extends StatefulWidget {
  final Usuario usuario;
  const HomeScreen({super.key, required this.usuario});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  int _index = 0;
  int _mapRevision = 0;
  int _favoritesRevision = 0;

  Future<void> _onNavTap(int i) async {
    if (i == 2) {
      final criado = await showCriarEventoSheet(context, widget.usuario);
      if (criado == true && mounted) {
        setState(() {
          _mapRevision++;
          _index = 1;
        });
        ScaffoldMessenger.of(context)
            .showSnackBar(const SnackBar(content: Text('Expedição criada e adicionada ao mapa!')));
      }
      return;
    }

    setState(() {
      _index = i;
      if (i == 1) _mapRevision++;
      if (i == 3) _favoritesRevision++;
    });
  }

  @override
  Widget build(BuildContext context) {
    final tabs = [
      HomeTab(usuario: widget.usuario),
      MapScreen(key: ValueKey('map-$_mapRevision'), usuario: widget.usuario),
      const SizedBox.shrink(),
      FavoritosTab(key: ValueKey('favorites-$_favoritesRevision'), usuario: widget.usuario),
      ProfileScreen(usuario: widget.usuario),
    ];

    return Scaffold(
      backgroundColor: AppColors.bgDark,
      body: IndexedStack(index: _index, children: tabs),
      bottomNavigationBar: AppBottomNav(currentIndex: _index, onTap: _onNavTap),
    );
  }
}
