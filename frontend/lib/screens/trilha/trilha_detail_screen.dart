import 'package:flutter/material.dart';
import 'package:intl/intl.dart';
import '../../core/theme/app_theme.dart';
import '../../models/usuario.dart';
import '../../models/trilha.dart';
import '../../models/avaliacao.dart';
import '../../models/evento.dart';
import '../../models/checkpoint.dart';
import '../../models/checklist_item.dart';
import '../../services/trilha_service.dart';
import '../../services/evento_service.dart';
import '../../services/checkpoint_service.dart';
import '../../services/favorito_service.dart';
import '../../services/checklist_service.dart';
import '../../services/historico_service.dart';
import '../../models/historico_trilha.dart';
import '../../widgets/difficulty_badge.dart';
import '../../widgets/evento_card.dart';
import '../../widgets/trail_map_widget.dart';

class TrilhaDetailScreen extends StatefulWidget {
  final int idTrilha;
  final Usuario usuario;

  const TrilhaDetailScreen({super.key, required this.idTrilha, required this.usuario});

  @override
  State<TrilhaDetailScreen> createState() => _TrilhaDetailScreenState();
}

class _TrilhaDetailScreenState extends State<TrilhaDetailScreen> {
  late Future<Trilha> _trilhaFuture;
  late Future<List<Avaliacao>> _avaliacoesFuture;
  late Future<List<Evento>> _eventosFuture;
  late Future<List<Checkpoint>> _checkpointsFuture;

  bool _favoritado = false;
  bool _iniciandoTrilha = false;
  bool _baixandoMapa = false;
  bool _trilhaEmAndamento = false;
  DateTime? _inicioTrilha;
  List<ChecklistItem> _checklist = [];
  int? _checklistTrilhaId;

  @override
  void initState() {
    super.initState();
    _carregarTudo();
  }

  void _carregarTudo() {
    _trilhaFuture = TrilhaService.buscarPorId(widget.idTrilha);
    _avaliacoesFuture = TrilhaService.listarAvaliacoes(widget.idTrilha);
    _eventosFuture = EventoService.listarPorTrilha(widget.idTrilha);
    _checkpointsFuture = CheckpointService.listarPorTrilha(widget.idTrilha);
    _carregarFavorito();
  }

  Future<void> _carregarFavorito() async {
    try {
      final favoritos = await FavoritoService.listar(widget.usuario.idUsuario!);
      if (mounted) {
        setState(() => _favoritado = favoritos.any((f) => f.idTrilha == widget.idTrilha));
      }
    } catch (_) {
    }
  }

  Future<void> _alternarFavorito() async {
    final novoValor = !_favoritado;
    setState(() => _favoritado = novoValor);
    try {
      if (novoValor) {
        await FavoritoService.adicionar(widget.idTrilha);
      } else {
        await FavoritoService.remover(widget.idTrilha);
      }
    } catch (_) {
      if (mounted) {
        setState(() => _favoritado = !novoValor);
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('Não foi possível atualizar os favoritos.')),
        );
      }
    }
  }

  Future<void> _iniciarTrilha() async {
    setState(() => _iniciandoTrilha = true);
    try {
      await CheckpointService.registrar(
        Checkpoint(latitude: 0.0, longitude: 0.0, horario: DateTime.now(), idTrilha: widget.idTrilha),
      );
      if (!mounted) return;
      setState(() {
        _trilhaEmAndamento = true;
        _inicioTrilha = DateTime.now();
      });
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Trilha iniciada! Toque em "Concluir" ao terminar.')),
      );
    } catch (_) {
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Não foi possível iniciar a trilha agora.')),
      );
    } finally {
      if (mounted) setState(() => _iniciandoTrilha = false);
    }
  }

  Future<void> _concluirTrilha() async {
    setState(() => _iniciandoTrilha = true);
    try {
      final tempoMin = _inicioTrilha != null
          ? DateTime.now().difference(_inicioTrilha!).inMinutes.toDouble()
          : null;
      await HistoricoService.registrar(HistoricoTrilha(
        idTrilha: widget.idTrilha,
        dataRealizacao: DateTime.now(),
        tempo: tempoMin,
      ));
      if (!mounted) return;
      setState(() {
        _trilhaEmAndamento = false;
        _inicioTrilha = null;
      });
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Trilha concluída! Registrada no seu histórico.')),
      );
    } catch (_) {
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Não foi possível registrar a trilha no histórico.')),
      );
    } finally {
      if (mounted) setState(() => _iniciandoTrilha = false);
    }
  }

  Future<void> _baixarMapaOffline() async {
    setState(() => _baixandoMapa = true);
    try {
      await CheckpointService.baixarMapaOffline(widget.idTrilha);
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Mapa offline baixado com sucesso.')),
      );
    } catch (_) {
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Falha ao baixar o mapa offline.')),
      );
    } finally {
      if (mounted) setState(() => _baixandoMapa = false);
    }
  }

  void _abrirAvaliacaoDialog() {
    int nota = 5;
    final comentarioController = TextEditingController();
    showDialog(
      context: context,
      builder: (ctx) => StatefulBuilder(
        builder: (ctx, setDialogState) => AlertDialog(
          backgroundColor: AppColors.bgCard,
          title: const Text('Avaliar trilha', style: TextStyle(color: AppColors.textPrimary)),
          content: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: List.generate(5, (i) {
                  final filled = i < nota;
                  return IconButton(
                    onPressed: () => setDialogState(() => nota = i + 1),
                    icon: Icon(filled ? Icons.star : Icons.star_border, color: AppColors.amber),
                  );
                }),
              ),
              TextField(
                controller: comentarioController,
                maxLines: 3,
                style: const TextStyle(color: AppColors.textPrimary),
                decoration: const InputDecoration(hintText: 'Conte como foi sua experiência...'),
              ),
            ],
          ),
          actions: [
            TextButton(onPressed: () => Navigator.pop(ctx), child: const Text('Cancelar')),
            ElevatedButton(
              onPressed: () async {
                if (widget.usuario.idUsuario == null) return;
                await TrilhaService.avaliar(Avaliacao(
                  nota: nota,
                  comentario: comentarioController.text.trim(),
                  idUsuario: widget.usuario.idUsuario!,
                  idTrilha: widget.idTrilha,
                ));
                if (ctx.mounted) Navigator.pop(ctx);
                setState(() => _avaliacoesFuture = TrilhaService.listarAvaliacoes(widget.idTrilha));
              },
              child: const Text('Enviar'),
            ),
          ],
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.bgDark,
      body: FutureBuilder<Trilha>(
        future: _trilhaFuture,
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            return const Center(child: CircularProgressIndicator(color: AppColors.greenLight));
          }
          if (snapshot.hasError || !snapshot.hasData) {
            return Center(
              child: Column(
                mainAxisSize: MainAxisSize.min,
                children: [
                  const Text('Não foi possível carregar esta trilha.',
                      style: TextStyle(color: AppColors.textDim)),
                  TextButton(onPressed: () => Navigator.pop(context), child: const Text('Voltar')),
                ],
              ),
            );
          }
          return _buildContent(snapshot.data!);
        },
      ),
    );
  }

  Widget _buildContent(Trilha trilha) {
    if (_checklistTrilhaId != trilha.idTrilha) {
      _checklistTrilhaId = trilha.idTrilha;
      _checklist = ChecklistService.gerarParaTrilha(trilha);
    }
    return Stack(
      children: [
        CustomScrollView(
          slivers: [
            SliverToBoxAdapter(child: _buildHeader(trilha)),
            SliverToBoxAdapter(child: _buildStats(trilha)),
            SliverToBoxAdapter(child: _buildMapa(trilha)),
            SliverToBoxAdapter(child: _buildSobre(trilha)),
            SliverToBoxAdapter(child: _buildChecklist(trilha)),
            SliverToBoxAdapter(child: _buildCheckpoints()),
            SliverToBoxAdapter(child: _buildEventos()),
            SliverToBoxAdapter(child: _buildAvaliacoes()),
            const SliverToBoxAdapter(child: SizedBox(height: 100)),
          ],
        ),
        Positioned(left: 0, right: 0, bottom: 0, child: _buildCtaBar()),
      ],
    );
  }

  Widget _buildHeader(Trilha trilha) {
    return SizedBox(
      height: 260,
      child: Stack(
        children: [
          Container(
            height: 260,
            width: double.infinity,
            color: AppColors.bgMid,
            child: trilha.imagemCapa != null
                ? Image.network(trilha.imagemCapa!, fit: BoxFit.cover)
                : const Center(child: Icon(Icons.terrain, color: AppColors.textDim, size: 56)),
          ),
          Container(
            height: 260,
            decoration: BoxDecoration(
              gradient: LinearGradient(
                begin: Alignment.topCenter,
                end: Alignment.bottomCenter,
                colors: [Colors.transparent, AppColors.bgDark.withOpacity(0.9)],
                stops: const [0.4, 1.0],
              ),
            ),
          ),
          SafeArea(
            child: Padding(
              padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
              child: Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  _circleButton(Icons.arrow_back, () => Navigator.pop(context)),
                  _circleButton(
                    _favoritado ? Icons.favorite : Icons.favorite_border,
                    _alternarFavorito,
                  ),
                ],
              ),
            ),
          ),
          Positioned(
            left: 24,
            bottom: 44,
            right: 24,
            child: Text(trilha.nome,
                style: const TextStyle(color: AppColors.textPrimary, fontSize: 24, fontWeight: FontWeight.bold)),
          ),
          Positioned(left: 24, bottom: 12, child: DifficultyBadge(dificuldade: trilha.dificuldade)),
        ],
      ),
    );
  }

  Widget _circleButton(IconData icon, VoidCallback onTap) {
    return GestureDetector(
      onTap: onTap,
      child: CircleAvatar(
        radius: 18,
        backgroundColor: Colors.black.withOpacity(0.45),
        child: Icon(icon, color: Colors.white, size: 18),
      ),
    );
  }

  Widget _buildStats(Trilha trilha) {
    final stats = [
      {'icon': Icons.straighten, 'val': '${trilha.distancia?.toStringAsFixed(1) ?? '--'} km', 'label': 'Distância'},
      {'icon': Icons.timer_outlined, 'val': trilha.duracaoFormatada, 'label': 'Duração'},
      {'icon': Icons.schedule, 'val': trilha.tempoEstimadoFormatado, 'label': 'Tempo est.'},
      {'icon': Icons.terrain, 'val': trilha.dificuldade ?? '--', 'label': 'Dificuldade'},
    ];
    return Padding(
      padding: const EdgeInsets.fromLTRB(16, 16, 16, 0),
      child: Row(
        children: stats.map((s) {
          return Expanded(
            child: Container(
              margin: const EdgeInsets.symmetric(horizontal: 4),
              padding: const EdgeInsets.symmetric(vertical: 12),
              decoration: BoxDecoration(color: AppColors.bgCard, borderRadius: BorderRadius.circular(12)),
              child: Column(
                children: [
                  Icon(s['icon'] as IconData, color: AppColors.greenLight, size: 18),
                  const SizedBox(height: 6),
                  Text(s['val'] as String,
                      style: const TextStyle(
                          color: AppColors.textPrimary, fontWeight: FontWeight.bold, fontSize: 12)),
                  Text(s['label'] as String, style: const TextStyle(color: AppColors.textDim, fontSize: 9)),
                ],
              ),
            ),
          );
        }).toList(),
      ),
    );
  }

  Widget _buildMapa(Trilha trilha) {
    return Padding(
      padding: const EdgeInsets.fromLTRB(24, 24, 24, 0),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Text('Mapa da Trilha',
              style: TextStyle(color: AppColors.textPrimary, fontSize: 15, fontWeight: FontWeight.bold)),
          const SizedBox(height: 4),
          const Text(
            'Rota com checkpoints registrados por trilheiros.',
            style: TextStyle(color: AppColors.textDim, fontSize: 12),
          ),
          const SizedBox(height: 10),
          FutureBuilder<List<Checkpoint>>(
            future: _checkpointsFuture,
            builder: (context, snapshot) {
              final checkpoints = snapshot.data ?? [];
              return TrailMapWidget(checkpoints: checkpoints, localizacao: trilha.localizacao);
            },
          ),
        ],
      ),
    );
  }

  Widget _buildChecklist(Trilha trilha) {
    final obrigatorios = _checklist.where((i) => i.obrigatorio).length;
    final concluidos = _checklist.where((i) => i.concluido).length;

    return Padding(
      padding: const EdgeInsets.fromLTRB(24, 24, 24, 0),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              const Text('Checklist de Equipamentos',
                  style: TextStyle(color: AppColors.textPrimary, fontSize: 15, fontWeight: FontWeight.bold)),
              Text(
                '$concluidos/${_checklist.length}',
                style: const TextStyle(color: AppColors.greenLight, fontSize: 12, fontWeight: FontWeight.bold),
              ),
            ],
          ),
          const SizedBox(height: 4),
          Text(
            '$obrigatorios itens obrigatórios para esta trilha.',
            style: const TextStyle(color: AppColors.textDim, fontSize: 12),
          ),
          const SizedBox(height: 10),
          ..._checklist.map((item) {
            return Container(
              margin: const EdgeInsets.only(bottom: 6),
              decoration: BoxDecoration(color: AppColors.bgCard, borderRadius: BorderRadius.circular(10)),
              child: CheckboxListTile(
                value: item.concluido,
                onChanged: (v) => setState(() => item.concluido = v ?? false),
                activeColor: AppColors.green,
                checkColor: Colors.white,
                dense: true,
                controlAffinity: ListTileControlAffinity.leading,
                title: Text(
                  item.descricao,
                  style: TextStyle(
                    color: item.concluido ? AppColors.textDim : AppColors.textPrimary,
                    fontSize: 13,
                    decoration: item.concluido ? TextDecoration.lineThrough : null,
                  ),
                ),
                subtitle: item.obrigatorio
                    ? const Text('Obrigatório', style: TextStyle(color: AppColors.amber, fontSize: 10))
                    : null,
              ),
            );
          }),
        ],
      ),
    );
  }

  Widget _buildSobre(Trilha trilha) {
    return Padding(
      padding: const EdgeInsets.fromLTRB(24, 24, 24, 0),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Text('Sobre a trilha',
              style: TextStyle(color: AppColors.textPrimary, fontSize: 15, fontWeight: FontWeight.bold)),
          if (trilha.localizacao != null && trilha.localizacao!.isNotEmpty) ...[
            const SizedBox(height: 6),
            Row(
              children: [
                const Icon(Icons.location_on, size: 14, color: AppColors.greenLight),
                const SizedBox(width: 4),
                Expanded(
                  child: Text(trilha.localizacao!,
                      style: const TextStyle(color: AppColors.textDim, fontSize: 12)),
                ),
              ],
            ),
          ],
          const SizedBox(height: 8),
          Text(
            trilha.descricao ?? 'Sem descrição cadastrada para esta trilha ainda.',
            style: const TextStyle(color: AppColors.textDim, fontSize: 13, height: 1.5),
          ),
        ],
      ),
    );
  }

  Widget _buildCheckpoints() {
    return Padding(
      padding: const EdgeInsets.fromLTRB(24, 24, 24, 0),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Text('Checkpoints registrados',
              style: TextStyle(color: AppColors.textPrimary, fontSize: 15, fontWeight: FontWeight.bold)),
          const SizedBox(height: 4),
          const Text(
            'Pontos confirmados via GPS por quem já percorreu esta trilha.',
            style: TextStyle(color: AppColors.textDim, fontSize: 12),
          ),
          const SizedBox(height: 10),
          FutureBuilder<List<Checkpoint>>(
            future: _checkpointsFuture,
            builder: (context, snapshot) {
              if (snapshot.connectionState == ConnectionState.waiting) {
                return const Padding(
                  padding: EdgeInsets.symmetric(vertical: 12),
                  child: LinearProgressIndicator(color: AppColors.greenLight, backgroundColor: AppColors.bgCard),
                );
              }
              final checkpoints = snapshot.data ?? [];
              if (checkpoints.isEmpty) {
                return const Text('Nenhum checkpoint registrado ainda. Seja o primeiro!',
                    style: TextStyle(color: AppColors.textDim, fontSize: 12));
              }
              return Wrap(
                spacing: 8,
                runSpacing: 8,
                children: checkpoints.take(6).map((c) {
                  return Container(
                    padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
                    decoration: BoxDecoration(color: AppColors.bgCard, borderRadius: BorderRadius.circular(10)),
                    child: Row(
                      mainAxisSize: MainAxisSize.min,
                      children: [
                        const Icon(Icons.location_on, size: 14, color: AppColors.greenLight),
                        const SizedBox(width: 6),
                        Text(
                          c.horario != null ? DateFormat('dd/MM HH:mm').format(c.horario!) : 'Sem horário',
                          style: const TextStyle(color: AppColors.textDim, fontSize: 11),
                        ),
                      ],
                    ),
                  );
                }).toList(),
              );
            },
          ),
        ],
      ),
    );
  }

  Widget _buildEventos() {
    return Padding(
      padding: const EdgeInsets.fromLTRB(24, 24, 24, 0),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Text('Eventos Próximos',
              style: TextStyle(color: AppColors.textPrimary, fontSize: 15, fontWeight: FontWeight.bold)),
          const SizedBox(height: 10),
          FutureBuilder<List<Evento>>(
            future: _eventosFuture,
            builder: (context, snapshot) {
              if (snapshot.connectionState == ConnectionState.waiting) {
                return const Padding(
                  padding: EdgeInsets.symmetric(vertical: 12),
                  child: LinearProgressIndicator(color: AppColors.greenLight, backgroundColor: AppColors.bgCard),
                );
              }
              final eventos = snapshot.data ?? [];
              if (eventos.isEmpty) {
                return const Text('Nenhum evento agendado para esta trilha ainda.',
                    style: TextStyle(color: AppColors.textDim, fontSize: 12));
              }
              return Column(
                children: eventos.map((e) {
                  return EventoCard(
                    evento: e,
                    onParticipar: () async {
                      if (e.idEvento == null || widget.usuario.idUsuario == null) return;
                      await EventoService.participar(e.idEvento!, widget.usuario.idUsuario!);
                      if (mounted) {
                        ScaffoldMessenger.of(context)
                            .showSnackBar(const SnackBar(content: Text('Você entrou no evento!')));
                      }
                    },
                  );
                }).toList(),
              );
            },
          ),
        ],
      ),
    );
  }

  Widget _buildAvaliacoes() {
    return Padding(
      padding: const EdgeInsets.fromLTRB(24, 24, 24, 0),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              const Text('Avaliações',
                  style: TextStyle(color: AppColors.textPrimary, fontSize: 15, fontWeight: FontWeight.bold)),
              TextButton(
                onPressed: _abrirAvaliacaoDialog,
                child: const Text('Avaliar', style: TextStyle(color: AppColors.greenLight)),
              ),
            ],
          ),
          FutureBuilder<List<Avaliacao>>(
            future: _avaliacoesFuture,
            builder: (context, snapshot) {
              if (snapshot.connectionState == ConnectionState.waiting) {
                return const Padding(
                  padding: EdgeInsets.symmetric(vertical: 12),
                  child: LinearProgressIndicator(color: AppColors.greenLight, backgroundColor: AppColors.bgCard),
                );
              }
              final avaliacoes = snapshot.data ?? [];
              if (avaliacoes.isEmpty) {
                return const Padding(
                  padding: EdgeInsets.symmetric(vertical: 8),
                  child: Text('Ainda não há avaliações. Seja o primeiro a avaliar!',
                      style: TextStyle(color: AppColors.textDim, fontSize: 12)),
                );
              }
              return Column(
                children: avaliacoes.map((a) {
                  return Container(
                    margin: const EdgeInsets.only(bottom: 10),
                    padding: const EdgeInsets.all(12),
                    decoration: BoxDecoration(color: AppColors.bgCard, borderRadius: BorderRadius.circular(12)),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Row(
                          children: [
                            Text(a.nomeUsuario ?? 'Usuário',
                                style: const TextStyle(
                                    color: AppColors.textPrimary, fontWeight: FontWeight.bold, fontSize: 12)),
                            const Spacer(),
                            Row(
                              children: List.generate(
                                5,
                                (i) =>
                                    Icon(i < a.nota ? Icons.star : Icons.star_border, size: 12, color: AppColors.amber),
                              ),
                            ),
                          ],
                        ),
                        if (a.comentario != null && a.comentario!.isNotEmpty) ...[
                          const SizedBox(height: 6),
                          Text(a.comentario!, style: const TextStyle(color: AppColors.textDim, fontSize: 12)),
                        ],
                      ],
                    ),
                  );
                }).toList(),
              );
            },
          ),
        ],
      ),
    );
  }

  Widget _buildCtaBar() {
    return Container(
      padding: const EdgeInsets.fromLTRB(24, 12, 24, 24),
      decoration: BoxDecoration(
        color: AppColors.bgDark,
        boxShadow: [BoxShadow(color: Colors.black.withOpacity(0.4), blurRadius: 16, offset: const Offset(0, -4))],
      ),
      child: Row(
        children: [
          Expanded(
            flex: 2,
            child: ElevatedButton.icon(
              onPressed: _iniciandoTrilha
                  ? null
                  : (_trilhaEmAndamento ? _concluirTrilha : _iniciarTrilha),
              icon: _iniciandoTrilha
                  ? const SizedBox(
                      height: 14, width: 14, child: CircularProgressIndicator(strokeWidth: 2, color: Colors.white))
                  : Icon(_trilhaEmAndamento ? Icons.flag : Icons.navigation, size: 18),
              label: Text(_trilhaEmAndamento ? 'Concluir Trilha' : 'Iniciar Trilha'),
            ),
          ),
          const SizedBox(width: 12),
          Expanded(
            child: OutlinedButton.icon(
              onPressed: _baixandoMapa ? null : _baixarMapaOffline,
              style: OutlinedButton.styleFrom(backgroundColor: AppColors.bgCard, side: BorderSide.none),
              icon: _baixandoMapa
                  ? const SizedBox(
                      height: 14,
                      width: 14,
                      child: CircularProgressIndicator(strokeWidth: 2, color: AppColors.greenLight))
                  : const Icon(Icons.download, size: 16, color: AppColors.greenLight),
              label: const Text('Mapa', style: TextStyle(fontSize: 12, color: AppColors.greenLight)),
            ),
          ),
        ],
      ),
    );
  }
}
