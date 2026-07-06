import 'package:flutter/material.dart';
import '../../core/theme/app_theme.dart';
import '../../models/usuario.dart';
import '../../models/evento.dart';
import '../../models/denuncia.dart';
import '../../services/evento_service.dart';
import '../../services/denuncia_service.dart';
import '../../widgets/evento_card.dart';

class MapScreen extends StatefulWidget {
  final Usuario usuario;
  const MapScreen({super.key, required this.usuario});

  @override
  State<MapScreen> createState() => _MapScreenState();
}

class _MapScreenState extends State<MapScreen> {
  late Future<List<Evento>> _eventosFuture;
  final _buscaController = TextEditingController();

  static const _posicoesDecorativas = [
    Alignment(-0.5, -0.5),
    Alignment(0.3, -0.2),
    Alignment(0.7, -0.7),
    Alignment(-0.2, 0.4),
  ];

  static const _coresDecorativas = [
    AppColors.greenLight,
    AppColors.amber,
    AppColors.red,
    AppColors.greenLight,
  ];

  @override
  void initState() {
    super.initState();
    _eventosFuture = EventoService.listarProximos();
  }

  @override
  void dispose() {
    _buscaController.dispose();
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

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.bgDark,
      body: SafeArea(
        child: Column(
          children: [
            _buildMapaIlustrativo(),
            Expanded(child: _buildDrawer()),
          ],
        ),
      ),
    );
  }

  Widget _buildMapaIlustrativo() {
    return SizedBox(
      height: 250,
      child: Stack(
        children: [
          Container(color: const Color(0xFF16201A)),
          CustomPaint(size: Size.infinite, painter: _GridPainter()),
          for (int i = 0; i < _posicoesDecorativas.length; i++)
            Align(
              alignment: _posicoesDecorativas[i],
              child: Container(
                width: 26,
                height: 26,
                decoration: BoxDecoration(
                  shape: BoxShape.circle,
                  color: _coresDecorativas[i].withOpacity(0.9),
                  border: Border.all(color: Colors.white24, width: 2),
                ),
                child: const Icon(Icons.hiking, size: 14, color: Colors.black87),
              ),
            ),
          const Align(alignment: Alignment(0, 0.3), child: _UserDot()),
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
                      color: AppColors.bgDark.withOpacity(0.9),
                      borderRadius: BorderRadius.circular(22),
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
                Container(
                  width: 44,
                  height: 44,
                  decoration: BoxDecoration(color: AppColors.green, borderRadius: BorderRadius.circular(22)),
                  child: const Icon(Icons.tune, color: Colors.white),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildDrawer() {
    return Container(
      width: double.infinity,
      decoration: const BoxDecoration(
        color: AppColors.bgDark,
        borderRadius: BorderRadius.vertical(top: Radius.circular(20)),
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
                const Text(
                  'Expedições Abertas Perto',
                  style: TextStyle(color: AppColors.textPrimary, fontSize: 15, fontWeight: FontWeight.bold),
                ),
                FutureBuilder<List<Evento>>(
                  future: _eventosFuture,
                  builder: (context, snapshot) {
                    final count = snapshot.data?.length ?? 0;
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
                if (snapshot.connectionState == ConnectionState.waiting) {
                  return const Center(child: CircularProgressIndicator(color: AppColors.greenLight));
                }
                if (snapshot.hasError) {
                  return const Center(
                    child: Text('Não foi possível carregar expedições.', style: TextStyle(color: AppColors.textDim)),
                  );
                }
                var eventos = snapshot.data ?? [];
                final busca = _buscaController.text.trim().toLowerCase();
                if (busca.isNotEmpty) {
                  eventos = eventos.where((e) => e.titulo.toLowerCase().contains(busca)).toList();
                }
                if (eventos.isEmpty) {
                  return const Center(
                    child: Text('Nenhuma expedição aberta encontrada.', style: TextStyle(color: AppColors.textDim)),
                  );
                }
                return ListView.builder(
                  padding: const EdgeInsets.fromLTRB(24, 0, 24, 24),
                  itemCount: eventos.length,
                  itemBuilder: (context, i) => EventoCard(
                    evento: eventos[i],
                    onParticipar: () async {
                      if (eventos[i].idEvento == null || widget.usuario.idUsuario == null) return;
                      await EventoService.participar(eventos[i].idEvento!, widget.usuario.idUsuario!);
                      if (mounted) {
                        ScaffoldMessenger.of(context)
                            .showSnackBar(const SnackBar(content: Text('Você entrou na expedição!')));
                      }
                    },
                    onReportar: () => _abrirDenunciaDialog(eventos[i]),
                  ),
                );
              },
            ),
          ),
        ],
      ),
    );
  }
}

class _UserDot extends StatelessWidget {
  const _UserDot();

  @override
  Widget build(BuildContext context) {
    return Stack(
      alignment: Alignment.center,
      children: [
        Container(
          width: 30,
          height: 30,
          decoration: BoxDecoration(
            shape: BoxShape.circle,
            border: Border.all(color: AppColors.blueUser.withOpacity(0.4), width: 2),
          ),
        ),
        Container(
          width: 14,
          height: 14,
          decoration: const BoxDecoration(shape: BoxShape.circle, color: AppColors.blueUser),
        ),
      ],
    );
  }
}

class _GridPainter extends CustomPainter {
  @override
  void paint(Canvas canvas, Size size) {
    final paint = Paint()
      ..color = AppColors.greenLight.withOpacity(0.08)
      ..strokeWidth = 1;
    for (double x = 0; x < size.width; x += size.width / 6) {
      canvas.drawLine(Offset(x, 0), Offset(x, size.height), paint);
    }
    for (double y = 0; y < size.height; y += size.height / 5) {
      canvas.drawLine(Offset(0, y), Offset(size.width, y), paint);
    }
  }

  @override
  bool shouldRepaint(covariant CustomPainter oldDelegate) => false;
}
