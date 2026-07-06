import 'package:flutter/material.dart';
import '../../core/theme/app_theme.dart';
import '../../models/trilha.dart';
import '../../models/usuario.dart';
import '../../services/favorito_service.dart';
import '../../services/trilha_service.dart';
import '../../widgets/trilha_card.dart';
import '../trilha/trilha_detail_screen.dart';

class FavoritosTab extends StatefulWidget {
  final Usuario usuario;
  const FavoritosTab({super.key, required this.usuario});

  @override
  State<FavoritosTab> createState() => _FavoritosTabState();
}

class _FavoritosTabState extends State<FavoritosTab> {
  late Future<List<Trilha>> _favoritasFuture;

  @override
  void initState() {
    super.initState();
    _carregar();
  }

  void _carregar() {
    _favoritasFuture = _buscarTrilhasFavoritas();
  }

  Future<List<Trilha>> _buscarTrilhasFavoritas() async {
    final favoritos = await FavoritoService.listar(widget.usuario.idUsuario!);
    final trilhas = await Future.wait(
      favoritos.map((f) => TrilhaService.buscarPorId(f.idTrilha)),
    );
    return trilhas;
  }

  Future<void> _remover(Trilha trilha) async {
    if (trilha.idTrilha == null) return;
    try {
      await FavoritoService.remover(trilha.idTrilha!);
      if (mounted) setState(_carregar);
    } catch (_) {
      if (mounted) {
        ScaffoldMessenger.of(context)
            .showSnackBar(const SnackBar(content: Text('Não foi possível remover dos favoritos.')));
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return SafeArea(
      child: RefreshIndicator(
        onRefresh: () async {
          setState(_carregar);
          await _favoritasFuture;
        },
        child: FutureBuilder<List<Trilha>>(
          future: _favoritasFuture,
          builder: (context, snapshot) {
            if (snapshot.connectionState == ConnectionState.waiting) {
              return const Center(child: CircularProgressIndicator());
            }
            final trilhas = snapshot.data ?? [];
            if (trilhas.isEmpty) {
              return ListView(
                physics: const AlwaysScrollableScrollPhysics(),
                children: const [
                  Padding(
                    padding: EdgeInsets.all(32),
                    child: Column(
                      mainAxisSize: MainAxisSize.min,
                      children: [
                        SizedBox(height: 80),
                        Icon(Icons.favorite_border, size: 48, color: AppColors.textDim),
                        SizedBox(height: 16),
                        Text(
                          'Suas trilhas favoritas vão aparecer aqui',
                          textAlign: TextAlign.center,
                          style: TextStyle(
                              color: AppColors.textPrimary, fontWeight: FontWeight.bold, fontSize: 15),
                        ),
                        SizedBox(height: 8),
                        Text(
                          'Toque no ♡ em qualquer trilha para salvá-la.',
                          textAlign: TextAlign.center,
                          style: TextStyle(color: AppColors.textDim, fontSize: 12),
                        ),
                      ],
                    ),
                  ),
                ],
              );
            }
            return GridView.builder(
              padding: const EdgeInsets.all(16),
              physics: const AlwaysScrollableScrollPhysics(),
              gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
                crossAxisCount: 2,
                mainAxisSpacing: 12,
                crossAxisSpacing: 12,
                childAspectRatio: 0.78,
              ),
              itemCount: trilhas.length,
              itemBuilder: (context, i) {
                final t = trilhas[i];
                return TrilhaCard(
                  trilha: t,
                  onTap: () {
                    if (t.idTrilha == null) return;
                    Navigator.push(
                      context,
                      MaterialPageRoute(
                        builder: (_) =>
                            TrilhaDetailScreen(idTrilha: t.idTrilha!, usuario: widget.usuario),
                      ),
                    ).then((_) => setState(_carregar));
                  },
                  onFavoritar: () => _remover(t),
                );
              },
            );
          },
        ),
      ),
    );
  }
}
