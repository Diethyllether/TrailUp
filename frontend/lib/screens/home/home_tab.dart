import 'package:flutter/material.dart';
import '../../core/theme/app_theme.dart';
import '../../models/usuario.dart';
import '../../models/trilha.dart';
import '../../models/evento.dart';
import '../../services/trilha_service.dart';
import '../../services/evento_service.dart';
import '../../services/favorito_service.dart';
import '../../widgets/trilha_card.dart';
import '../../widgets/evento_card.dart';
import '../trilha/trilha_detail_screen.dart';

class HomeTab extends StatefulWidget {
  final Usuario usuario;
  const HomeTab({super.key, required this.usuario});

  @override
  State<HomeTab> createState() => _HomeTabState();
}

class _HomeTabState extends State<HomeTab> {
  final _buscaController = TextEditingController();
  String _dificuldadeSelecionada = 'Todas';

  late Future<List<Trilha>> _trilhasFuture;
  late Future<List<Evento>> _eventosFuture;

  static const _filtros = ['Todas', 'Fácil', 'Moderado', 'Difícil'];

  @override
  void initState() {
    super.initState();
    _carregar();
  }

  @override
  void dispose() {
    _buscaController.dispose();
    super.dispose();
  }

  void _carregar() {
    _trilhasFuture = TrilhaService.listar(
      busca: _buscaController.text.trim(),
      dificuldade: _dificuldadeSelecionada,
    );
    _eventosFuture = EventoService.listarProximos();
  }

  Future<void> _refresh() async {
    setState(_carregar);
    await Future.wait([_trilhasFuture, _eventosFuture]);
  }

  @override
  Widget build(BuildContext context) {
    final primeiroNome = widget.usuario.nome.split(' ').first;
    return SafeArea(
      child: RefreshIndicator(
        color: AppColors.greenLight,
        backgroundColor: AppColors.bgCard,
        onRefresh: _refresh,
        child: CustomScrollView(
          slivers: [
            SliverToBoxAdapter(
              child: Padding(
                padding: const EdgeInsets.fromLTRB(24, 16, 24, 0),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text('Olá, $primeiroNome 👋',
                        style: const TextStyle(
                            color: AppColors.textPrimary, fontSize: 22, fontWeight: FontWeight.bold)),
                    const SizedBox(height: 4),
                    const Text('Onde vai trilhar hoje?', style: TextStyle(color: AppColors.textDim, fontSize: 14)),
                    const SizedBox(height: 20),
                    TextField(
                      controller: _buscaController,
                      onSubmitted: (_) => setState(_carregar),
                      style: const TextStyle(color: AppColors.textPrimary),
                      decoration: InputDecoration(
                        hintText: 'Buscar trilha ou região...',
                        prefixIcon: const Icon(Icons.search, color: AppColors.textDim),
                        suffixIcon: IconButton(
                          icon: const Icon(Icons.tune, color: AppColors.textDim, size: 20),
                          onPressed: () => setState(_carregar),
                        ),
                      ),
                    ),
                    const SizedBox(height: 16),
                    SizedBox(
                      height: 36,
                      child: ListView.separated(
                        scrollDirection: Axis.horizontal,
                        itemCount: _filtros.length,
                        separatorBuilder: (_, __) => const SizedBox(width: 8),
                        itemBuilder: (context, i) {
                          final f = _filtros[i];
                          final selected = f == _dificuldadeSelecionada;
                          return ChoiceChip(
                            label: Text(f),
                            selected: selected,
                            onSelected: (_) => setState(() {
                              _dificuldadeSelecionada = f;
                              _carregar();
                            }),
                            selectedColor: AppColors.green,
                            backgroundColor: AppColors.bgCard,
                            labelStyle: TextStyle(
                              color: selected ? Colors.white : AppColors.textDim,
                              fontWeight: selected ? FontWeight.bold : FontWeight.normal,
                              fontSize: 12,
                            ),
                            shape: RoundedRectangleBorder(
                                borderRadius: BorderRadius.circular(16), side: BorderSide.none),
                          );
                        },
                      ),
                    ),
                    const SizedBox(height: 24),
                    const Text('Trilhas em Destaque',
                        style: TextStyle(color: AppColors.textPrimary, fontSize: 16, fontWeight: FontWeight.bold)),
                  ],
                ),
              ),
            ),
            SliverToBoxAdapter(
              child: SizedBox(
                height: 230,
                child: FutureBuilder<List<Trilha>>(
                  future: _trilhasFuture,
                  builder: (context, snapshot) {
                    if (snapshot.connectionState == ConnectionState.waiting) {
                      return const Center(child: CircularProgressIndicator(color: AppColors.greenLight));
                    }
                    if (snapshot.hasError) {
                      return _mensagem('Não foi possível carregar as trilhas.');
                    }
                    final trilhas = snapshot.data ?? [];
                    if (trilhas.isEmpty) {
                      return _mensagem('Nenhuma trilha encontrada.');
                    }
                    return ListView.separated(
                      padding: const EdgeInsets.symmetric(horizontal: 24),
                      scrollDirection: Axis.horizontal,
                      itemCount: trilhas.length,
                      separatorBuilder: (_, __) => const SizedBox(width: 12),
                      itemBuilder: (context, i) {
                        final t = trilhas[i];
                        return TrilhaCard(
                          trilha: t,
                          onTap: () {
                            if (t.idTrilha == null) return;
                            Navigator.push(
                              context,
                              MaterialPageRoute(
                                builder: (_) => TrilhaDetailScreen(idTrilha: t.idTrilha!, usuario: widget.usuario),
                              ),
                            );
                          },
                          onFavoritar: t.idTrilha == null
                              ? null
                              : () async {
                                  try {
                                    await FavoritoService.adicionar(t.idTrilha!);
                                    if (mounted) {
                                      ScaffoldMessenger.of(context).showSnackBar(
                                        const SnackBar(content: Text('Trilha salva nos favoritos.')),
                                      );
                                    }
                                  } catch (_) {
                                    if (mounted) {
                                      ScaffoldMessenger.of(context).showSnackBar(
                                        const SnackBar(content: Text('Não foi possível favoritar agora.')),
                                      );
                                    }
                                  }
                                },
                        );
                      },
                    );
                  },
                ),
              ),
            ),
            SliverToBoxAdapter(
              child: Padding(
                padding: const EdgeInsets.fromLTRB(24, 24, 24, 8),
                child: Text('Expedições Ativas',
                    style: const TextStyle(color: AppColors.textPrimary, fontSize: 16, fontWeight: FontWeight.bold)),
              ),
            ),
            SliverPadding(
              padding: const EdgeInsets.fromLTRB(24, 0, 24, 100),
              sliver: FutureBuilder<List<Evento>>(
                future: _eventosFuture,
                builder: (context, snapshot) {
                  if (snapshot.connectionState == ConnectionState.waiting) {
                    return const SliverToBoxAdapter(
                      child: Padding(
                        padding: EdgeInsets.symmetric(vertical: 24),
                        child: Center(child: CircularProgressIndicator(color: AppColors.greenLight)),
                      ),
                    );
                  }
                  if (snapshot.hasError) {
                    return SliverToBoxAdapter(child: _mensagem('Não foi possível carregar expedições.'));
                  }
                  final eventos = snapshot.data ?? [];
                  if (eventos.isEmpty) {
                    return SliverToBoxAdapter(child: _mensagem('Nenhuma expedição aberta perto de você.'));
                  }
                  return SliverList(
                    delegate: SliverChildBuilderDelegate(
                      (context, i) {
                        final e = eventos[i];
                        return EventoCard(
                          evento: e,
                          onParticipar: () async {
                            if (e.idEvento == null || widget.usuario.idUsuario == null) return;
                            await EventoService.participar(e.idEvento!, widget.usuario.idUsuario!);
                            if (context.mounted) {
                              ScaffoldMessenger.of(context)
                                  .showSnackBar(const SnackBar(content: Text('Você entrou na expedição!')));
                            }
                          },
                        );
                      },
                      childCount: eventos.length,
                    ),
                  );
                },
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _mensagem(String msg) => Padding(
        padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 16),
        child: Text(msg, style: const TextStyle(color: AppColors.textDim)),
      );
}
