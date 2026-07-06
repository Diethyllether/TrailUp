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

  Future<void> _onNavTap(int i) async {
    if (i == 2) {
      final criado = await showCriarEventoSheet(context, widget.usuario);
      if (criado == true && mounted) {
        ScaffoldMessenger.of(context)
            .showSnackBar(const SnackBar(content: Text('Expedição criada com sucesso!')));
      }
      return;
    }
    setState(() => _index = i);
  }

  @override
  Widget build(BuildContext context) {
    final tabs = [
      HomeTab(usuario: widget.usuario),
      MapScreen(usuario: widget.usuario),
      const SizedBox.shrink(),
      FavoritosTab(usuario: widget.usuario),
      ProfileScreen(usuario: widget.usuario),
    ];

    return Scaffold(
      backgroundColor: AppColors.bgDark,
      body: IndexedStack(index: _index, children: tabs),
      bottomNavigationBar: AppBottomNav(currentIndex: _index, onTap: _onNavTap),
    );
  }
}
