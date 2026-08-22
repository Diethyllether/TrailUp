import 'dart:async';

import 'package:flutter/material.dart';
import 'package:latlong2/latlong.dart';
import '../../core/theme/app_theme.dart';
import '../../models/usuario.dart';
import '../../models/evento.dart';
import '../../models/denuncia.dart';
import '../../models/checkpoint.dart';
import '../../services/evento_service.dart';
import '../../services/denuncia_service.dart';
import '../../services/checkpoint_service.dart';
import '../../services/trilha_service.dart';
import '../../widgets/evento_card.dart';
import '../../widgets/satellite_map_widget.dart';
import '../../widgets/trail_map_widget.dart';

class MapScreen extends StatefulWidget {
  final Usuario usuario;
  const MapScreen({super.key, required this.usuario});

  @override
  State<MapScreen> createState() => _MapScreenState();
}

class _MapScreenState extends State<MapScreen> with WidgetsBindingObserver {
  late Future<List<Evento>> _eventosFuture;
  final _buscaController = TextEditingController();
  final _listScrollController = ScrollController();
  Timer? _refreshTimer;
  bool _satellite = true;
  int? _eventoSelecionado;

  Evento? _expedicaoAtiva;
  Future<List<Checkpoint>>? _checkpointsExpedicaoFuture;
  String? _localizacaoExpedicao;

  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addObserver(this);
    _eventosFuture = EventoService.listarProximos(apenasNoMapa: true);
    _refreshTimer = Timer.periodic(
      const Duration(seconds: 5),
      (_) => _recarregarEventos(),
    );
  }

  @override
  void didChangeAppLifecycleState(AppLifecycleState state) {
    if (state == AppLifecycleState.resumed) {
      _recarregarEventos();
    }
  }

  void _recarregarEventos() {
    if (!mounted) return;
    setState(() {
      _eventosFuture = EventoService.listarProximos(apenasNoMapa: true);
    });
  }

  Future<void> _ativarExpedicao(Evento evento) async {
    final idsTrilhas = evento.trilhasIds ?? const <int>[];
    if (idsTrilhas.isEmpty) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('Esta expedição não possui uma trilha vinculada.')),
        );
      }
      return;
    }

    final idTrilha = idsTrilhas.first;
    setState(() {
      _expedicaoAtiva = evento;
      _eventoSelecionado = evento.idEvento;
      _checkpointsExpedicaoFuture = CheckpointService.listarPorTrilha(idTrilha);
      _localizacaoExpedicao = null;
    });

    try {
      final trilha = await TrilhaService.buscarPorId(idTrilha);
      if (mounted && _expedicaoAtiva?.idEvento == evento.idEvento) {
        setState(() => _localizacaoExpedicao = trilha.localizacao);
      }
    } catch (_) {
      // O mapa continua funcional mesmo sem o nome textual da localização.
    }
  }

  void _sairDoFocoDaExpedicao() {
    setState(() {
      _expedicaoAtiva = null;
      _checkpointsExpedicaoFuture = null;
      _localizacaoExpedicao = null;
    });
    _recarregarEventos();
  }

  @override
  void dispose() {
    WidgetsBinding.instance.removeObserver(this);
    _refreshTimer?.cancel();
    _buscaController.dispose();
    _listScrollController.dispose();
    super.dispose();
  }

  void _abrirDenunciaDialog(Evento evento) {
    final controller = TextEditingController();
    showDialog(
      context: context,
      builder: (ctx) => AlertDialog(
        backgroundColor: AppColors.bgCard,
        title: const Text('Reportar expedição', style: TextStyle(color: AppColors.textPrimary)),
        content: TextField(
          controller: controller,
          maxLines: 3,
          style: const TextStyle(color: AppColors.textPrimary),
          decoration: const InputDecoration(hintText: 'Descreva o comportamento inadequado...'),
        ),
        actions: [
          TextButton(onPressed: () => Navigator.pop(ctx), child: const Text('Cancelar')),
          ElevatedButton(
            onPressed: () async {
              if (evento.idEvento != null && controller.text.trim().isNotEmpty) {
                await DenunciaService.criar(
                  Denuncia(descricao: controller.text.trim(), idEvento: evento.idEvento!),
                );
              }
              if (ctx.mounted) Navigator.pop(ctx);
            },
            child: const Text('Enviar'),
          ),
        ],
      ),
    );
  }

  List<Evento> _filtrarEventos(List<Evento> eventos) {
    final busca = _buscaController.text.trim().toLowerCase();
    if (busca.isEmpty) return eventos;
    return eventos.where((e) => e.titulo.toLowerCase().contains(busca)).toList();
  }

  List<MapPin> _pinsDeEventos(List<Evento> eventos) {
    return eventos
        .where((e) => e.latitude != null && e.longitude != null)
        .map((e) {
          final id = e.idEvento;
          final selecionado = id != null && id == _eventoSelecionado;
          return MapPin(
            position: LatLng(e.latitude!, e.longitude!),
            label: e.titulo.length > 18 ? '${e.titulo.substring(0, 18)}…' : e.titulo,
            color: selecionado ? AppColors.amber : AppColors.greenLight,
            icon: Icons.groups,
            onTap: () {
              setState(() => _eventoSelecionado = id);
              _scrollParaEvento(eventos.indexOf(e));
            },
          );
        })
        .toList();
  }

  String _assinaturaDosEventos(List<Evento> eventos) {
    final partes = eventos
        .where((e) => e.latitude != null && e.longitude != null)
        .map((e) => '${e.idEvento}:${e.latitude!.toStringAsFixed(6)}:${e.longitude!.toStringAsFixed(6)}')
        .toList()
      ..sort();
    return partes.join('|');
  }

  void _scrollParaEvento(int index) {
    if (index < 0) return;
    WidgetsBinding.instance.addPostFrameCallback((_) {
      if (!_listScrollController.hasClients) return;
      _listScrollController.animateTo(
        index * 120.0,
        duration: const Duration(milliseconds: 300),
        curve: Curves.easeOut,
      );
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.bgDark,
      body: SafeArea(
        child: Column(
          children: [
            Expanded(child: _buildMapa()),
            SizedBox(height: MediaQuery.of(context).size.height * 0.34, child: _buildDrawer()),
          ],
        ),
      ),
    );
  }

  Widget _buildMapa() {
    if (_expedicaoAtiva != null && _checkpointsExpedicaoFuture != null) {
      return _buildMapaExpedicaoAtiva();
    }

    return FutureBuilder<List<Evento>>(
      future: _eventosFuture,
      builder: (context, snapshot) {
        final eventos = _filtrarEventos(snapshot.data ?? []);
        final pins = _pinsDeEventos(eventos);
        final assinatura = _assinaturaDosEventos(eventos);

        return Stack(
          children: [
            Positioned.fill(
              child: SatelliteMapWidget(
                key: ValueKey('map-${_satellite}-$_eventoSelecionado-$assinatura'),
                pins: pins,
                satellite: _satellite,
                fitBounds: pins.isNotEmpty,
                fitPadding: const EdgeInsets.fromLTRB(48, 100, 48, 48),
              ),
            ),
            Positioned(
              left: 16,
              right: 16,
              top: 12,
              child: Row(
                children: [
                  Expanded(
                    child: Container(
                      height: 44,
                      padding: const EdgeInsets.symmetric(horizontal: 14),
                      decoration: BoxDecoration(
                        color: AppColors.bgDark.withOpacity(0.92),
                        borderRadius: BorderRadius.circular(22),
                        boxShadow: [
                          BoxShadow(color: Colors.black.withOpacity(0.25), blurRadius: 8, offset: const Offset(0, 2)),
                        ],
                      ),
                      child: Row(
                        children: [
                          const Icon(Icons.search, size: 18, color: AppColors.textDim),
                          const SizedBox(width: 8),
                          Expanded(
                            child: TextField(
                              controller: _buscaController,
                              onChanged: (_) => setState(() {}),
                              style: const TextStyle(color: AppColors.textPrimary, fontSize: 13),
                              decoration: const InputDecoration(
                                hintText: 'Buscar expedição no mapa...',
                                border: InputBorder.none,
                                isDense: true,
                              ),
                            ),
                          ),
                        ],
                      ),
                    ),
                  ),
                  const SizedBox(width: 10),
                  GestureDetector(
                    onTap: _recarregarEventos,
                    child: Container(
                      width: 44,
                      height: 44,
                      decoration: BoxDecoration(
                        color: AppColors.bgDark.withOpacity(0.92),
                        borderRadius: BorderRadius.circular(22),
                      ),
                      child: const Icon(Icons.refresh, color: AppColors.greenLight, size: 20),
                    ),
                  ),
                  const SizedBox(width: 10),
                  _MapToggleButton(
                    satellite: _satellite,
                    onToggle: () => setState(() => _satellite = !_satellite),
                  ),
                ],
              ),
            ),
            if (snapshot.connectionState == ConnectionState.waiting)
              const Positioned(
                top: 70,
                left: 0,
                right: 0,
                child: Center(
                  child: Card(
                    color: AppColors.bgCard,
                    child: Padding(
                      padding: EdgeInsets.symmetric(horizontal: 16, vertical: 8),
                      child: Text('Atualizando expedições…', style: TextStyle(color: AppColors.textDim, fontSize: 12)),
                    ),
                  ),
                ),
              ),
          ],
        );
      },
    );
  }

  Widget _buildMapaExpedicaoAtiva() {
    final evento = _expedicaoAtiva!;
    return Stack(
      children: [
        Positioned.fill(
          child: FutureBuilder<List<Checkpoint>>(
            future: _checkpointsExpedicaoFuture,
            builder: (context, snapshot) {
              if (snapshot.connectionState == ConnectionState.waiting) {
                return const Center(child: CircularProgressIndicator(color: AppColors.greenLight));
              }
              if (snapshot.hasError) {
                return const Center(
                  child: Text('Não foi possível carregar os checkpoints da expedição.',
                      style: TextStyle(color: AppColors.textDim)),
                );
              }
              return TrailMapWidget(
                key: ValueKey('expedicao-${evento.idEvento}-${snapshot.data?.length ?? 0}'),
                checkpoints: snapshot.data ?? const <Checkpoint>[],
                localizacao: _localizacaoExpedicao,
              );
            },
          ),
        ),
        Positioned(
          left: 16,
          right: 16,
          top: 12,
          child: Container(
            padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 10),
            decoration: BoxDecoration(
              color: AppColors.bgDark.withOpacity(0.94),
              borderRadius: BorderRadius.circular(14),
              boxShadow: [
                BoxShadow(color: Colors.black.withOpacity(0.3), blurRadius: 8, offset: const Offset(0, 2)),
              ],
            ),
            child: Row(
              children: [
                const Icon(Icons.navigation, color: AppColors.greenLight, size: 20),
                const SizedBox(width: 10),
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    mainAxisSize: MainAxisSize.min,
                    children: [
                      const Text('Expedição ativa',
                          style: TextStyle(color: AppColors.greenLight, fontSize: 10, fontWeight: FontWeight.bold)),
                      Text(
                        evento.titulo,
                        maxLines: 1,
                        overflow: TextOverflow.ellipsis,
                        style: const TextStyle(color: AppColors.textPrimary, fontSize: 13, fontWeight: FontWeight.bold),
                      ),
                    ],
                  ),
                ),
                IconButton(
                  tooltip: 'Voltar ao mapa geral',
                  onPressed: _sairDoFocoDaExpedicao,
                  icon: const Icon(Icons.close, color: AppColors.textDim),
                ),
              ],
            ),
          ),
        ),
      ],
    );
  }

  Widget _buildDrawer() {
    return Container(
      width: double.infinity,
      decoration: const BoxDecoration(
        color: AppColors.bgDark,
        borderRadius: BorderRadius.vertical(top: Radius.circular(20)),
        boxShadow: [BoxShadow(color: Colors.black26, blurRadius: 12, offset: Offset(0, -4))],
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Center(
            child: Container(
              margin: const EdgeInsets.symmetric(vertical: 10),
              width: 40,
              height: 4,
              decoration: BoxDecoration(
                color: AppColors.textDim.withOpacity(0.4),
                borderRadius: BorderRadius.circular(2),
              ),
            ),
          ),
          Padding(
            padding: const EdgeInsets.symmetric(horizontal: 24),
            child: Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Text(
                  _expedicaoAtiva != null ? 'Expedição em andamento' : 'Expedições Abertas Perto',
                  style: const TextStyle(color: AppColors.textPrimary, fontSize: 15, fontWeight: FontWeight.bold),
                ),
                if (_expedicaoAtiva == null)
                  FutureBuilder<List<Evento>>(
                    future: _eventosFuture,
                    builder: (context, snapshot) {
                      final count = _filtrarEventos(snapshot.data ?? []).length;
                      return Text('$count encontradas',
                          style: const TextStyle(color: AppColors.greenLight, fontSize: 11));
                    },
                  ),
              ],
            ),
          ),
          const SizedBox(height: 8),
          Expanded(
            child: FutureBuilder<List<Evento>>(
              future: _eventosFuture,
              builder: (context, snapshot) {
                if (snapshot.connectionState == ConnectionState.waiting && !snapshot.hasData) {
                  return const Center(child: CircularProgressIndicator(color: AppColors.greenLight));
                }
                if (snapshot.hasError) {
                  return const Center(
                    child: Text('Não foi possível carregar expedições.', style: TextStyle(color: AppColors.textDim)),
                  );
                }

                final todos = _filtrarEventos(snapshot.data ?? []);
                final eventos = _expedicaoAtiva == null
                    ? todos
                    : todos.where((e) => e.idEvento == _expedicaoAtiva!.idEvento).toList();

                if (eventos.isEmpty) {
                  return const Center(
                    child: Text('Nenhuma expedição aberta encontrada.', style: TextStyle(color: AppColors.textDim)),
                  );
                }
                return ListView.builder(
                  controller: _listScrollController,
                  padding: const EdgeInsets.fromLTRB(24, 0, 24, 24),
                  itemCount: eventos.length,
                  itemBuilder: (context, i) {
                    final e = eventos[i];
                    final selecionado = e.idEvento == _eventoSelecionado;
                    return Container(
                      decoration: selecionado
                          ? BoxDecoration(
                              borderRadius: BorderRadius.circular(14),
                              border: Border.all(color: AppColors.amber.withOpacity(0.6), width: 1.5),
                            )
                          : null,
                      margin: const EdgeInsets.only(bottom: 4),
                      child: EventoCard(
                        evento: e,
                        onParticipar: _expedicaoAtiva != null
                            ? null
                            : () async {
                                if (e.idEvento == null || widget.usuario.idUsuario == null) return;
                                await EventoService.participar(e.idEvento!, widget.usuario.idUsuario!);
                                await _ativarExpedicao(e);
                                _recarregarEventos();
                                if (mounted) {
                                  ScaffoldMessenger.of(context).showSnackBar(
                                    const SnackBar(content: Text('Você entrou na expedição. Mapa focado na trilha.')),
                                  );
                                }
                              },
                        onReportar: () => _abrirDenunciaDialog(e),
                      ),
                    );
                  },
                );
              },
            ),
          ),
        ],
      ),
    );
  }
}

class _MapToggleButton extends StatelessWidget {
  final bool satellite;
  final VoidCallback onToggle;

  const _MapToggleButton({required this.satellite, required this.onToggle});

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: onToggle,
      child: Container(
        width: 44,
        height: 44,
        decoration: BoxDecoration(
          color: AppColors.green,
          borderRadius: BorderRadius.circular(22),
          boxShadow: [
            BoxShadow(color: Colors.black.withOpacity(0.25), blurRadius: 8, offset: const Offset(0, 2)),
          ],
        ),
        child: Icon(
          satellite ? Icons.map_outlined : Icons.satellite_alt,
          color: Colors.white,
          size: 20,
        ),
      ),
    );
  }
}
