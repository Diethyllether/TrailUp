import 'package:flutter/material.dart';
import 'package:intl/intl.dart';
import '../core/theme/app_theme.dart';
import '../models/usuario.dart';
import '../models/trilha.dart';
import '../models/evento.dart';
import '../services/trilha_service.dart';
import '../services/evento_service.dart';
import '../services/checkpoint_service.dart';

Future<bool?> showCriarEventoSheet(BuildContext context, Usuario usuario) {
  return showModalBottomSheet<bool>(
    context: context,
    isScrollControlled: true,
    backgroundColor: Colors.transparent,
    builder: (_) => _CriarEventoSheet(usuario: usuario),
  );
}

class _CriarEventoSheet extends StatefulWidget {
  final Usuario usuario;
  const _CriarEventoSheet({required this.usuario});

  @override
  State<_CriarEventoSheet> createState() => _CriarEventoSheetState();
}

class _CriarEventoSheetState extends State<_CriarEventoSheet> {
  final _tituloController = TextEditingController();
  final _vagasController = TextEditingController(text: '6');
  DateTime? _dataHora;
  TipoEvento _tipo = TipoEvento.grupo;
  Trilha? _trilhaSelecionada;
  bool _salvando = false;

  late final Future<List<Trilha>> _trilhasFuture;

  @override
  void initState() {
    super.initState();
    _trilhasFuture = TrilhaService.listar();
  }

  @override
  void dispose() {
    _tituloController.dispose();
    _vagasController.dispose();
    super.dispose();
  }

  Future<void> _escolherDataHora() async {
    final data = await showDatePicker(
      context: context,
      initialDate: DateTime.now().add(const Duration(days: 1)),
      firstDate: DateTime.now(),
      lastDate: DateTime.now().add(const Duration(days: 365)),
    );
    if (data == null || !mounted) return;
    final hora = await showTimePicker(context: context, initialTime: const TimeOfDay(hour: 7, minute: 0));
    if (hora == null) return;
    setState(() => _dataHora = DateTime(data.year, data.month, data.day, hora.hour, hora.minute));
  }

  bool _coordenadaValida(double lat, double lng) {
    return lat >= -90 && lat <= 90 && lng >= -180 && lng <= 180 && !(lat == 0 && lng == 0);
  }

  Future<(double?, double?)> _coordenadasDaTrilha(int idTrilha) async {
    try {
      final checkpoints = await CheckpointService.listarPorTrilha(idTrilha);
      for (final checkpoint in checkpoints) {
        if (_coordenadaValida(checkpoint.latitude, checkpoint.longitude)) {
          return (checkpoint.latitude, checkpoint.longitude);
        }
      }
    } catch (_) {
      // O backend ainda possui fallback próprio; a criação não deve falhar
      // apenas porque a consulta de checkpoints falhou no cliente.
    }
    return (null, null);
  }

  Future<void> _salvar() async {
    if (_tituloController.text.trim().isEmpty || _trilhaSelecionada == null || _dataHora == null) {
      ScaffoldMessenger.of(context)
          .showSnackBar(const SnackBar(content: Text('Preencha trilha, título e data/hora.')));
      return;
    }

    final idTrilha = _trilhaSelecionada!.idTrilha;
    if (idTrilha == null) {
      ScaffoldMessenger.of(context)
          .showSnackBar(const SnackBar(content: Text('A trilha selecionada não possui um identificador válido.')));
      return;
    }

    setState(() => _salvando = true);
    try {
      final (latitude, longitude) = await _coordenadasDaTrilha(idTrilha);

      await EventoService.criar(
        Evento(
          titulo: _tituloController.text.trim(),
          data: _dataHora,
          vagas: int.tryParse(_vagasController.text) ?? 6,
          tipo: _tipo,
          latitude: latitude,
          longitude: longitude,
          idCriador: widget.usuario.idUsuario!,
        ),
        [idTrilha],
      );
      if (mounted) Navigator.pop(context, true);
    } catch (_) {
      if (mounted) {
        ScaffoldMessenger.of(context)
            .showSnackBar(const SnackBar(content: Text('Não foi possível criar a expedição.')));
      }
    } finally {
      if (mounted) setState(() => _salvando = false);
    }
  }

  Widget _tipoButton(String label, TipoEvento tipo) {
    final selected = _tipo == tipo;
    return GestureDetector(
      onTap: () => setState(() => _tipo = tipo),
      child: Container(
        padding: const EdgeInsets.symmetric(vertical: 14),
        alignment: Alignment.center,
        decoration: BoxDecoration(
          color: selected ? AppColors.green : AppColors.bgCard,
          borderRadius: BorderRadius.circular(12),
        ),
        child: Text(
          label,
          style: TextStyle(
            fontSize: 12,
            color: selected ? Colors.white : AppColors.textDim,
            fontWeight: selected ? FontWeight.bold : FontWeight.normal,
          ),
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: EdgeInsets.only(bottom: MediaQuery.of(context).viewInsets.bottom),
      child: Container(
        decoration: const BoxDecoration(
          color: AppColors.bgDark,
          borderRadius: BorderRadius.vertical(top: Radius.circular(20)),
        ),
        padding: const EdgeInsets.fromLTRB(24, 12, 24, 24),
        child: SingleChildScrollView(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            mainAxisSize: MainAxisSize.min,
            children: [
              Center(
                child: Container(
                  width: 40,
                  height: 4,
                  margin: const EdgeInsets.only(bottom: 16),
                  decoration: BoxDecoration(
                    color: AppColors.textDim.withOpacity(0.4),
                    borderRadius: BorderRadius.circular(2),
                  ),
                ),
              ),
              const Text(
                'Nova Expedição',
                style: TextStyle(color: AppColors.textPrimary, fontSize: 18, fontWeight: FontWeight.bold),
              ),
              const SizedBox(height: 4),
              const Text(
                'Crie uma sala de trilha para outros usuários entrarem.',
                style: TextStyle(color: AppColors.textDim, fontSize: 12),
              ),
              const SizedBox(height: 20),
              FutureBuilder<List<Trilha>>(
                future: _trilhasFuture,
                builder: (context, snapshot) {
                  final trilhas = snapshot.data ?? [];
                  return DropdownButtonFormField<Trilha>(
                    value: _trilhaSelecionada,
                    dropdownColor: AppColors.bgCard,
                    style: const TextStyle(color: AppColors.textPrimary, fontSize: 13),
                    decoration: InputDecoration(
                      hintText: snapshot.connectionState == ConnectionState.waiting
                          ? 'Carregando trilhas...'
                          : 'Selecione a trilha',
                    ),
                    items: trilhas.map((t) => DropdownMenuItem(value: t, child: Text(t.nome))).toList(),
                    onChanged: (t) => setState(() => _trilhaSelecionada = t),
                  );
                },
              ),
              const SizedBox(height: 14),
              TextField(
                controller: _tituloController,
                style: const TextStyle(color: AppColors.textPrimary),
                decoration: const InputDecoration(hintText: 'Título da expedição'),
              ),
              const SizedBox(height: 14),
              GestureDetector(
                onTap: _escolherDataHora,
                child: Container(
                  width: double.infinity,
                  padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 14),
                  decoration: BoxDecoration(color: AppColors.bgCard, borderRadius: BorderRadius.circular(14)),
                  child: Row(
                    children: [
                      const Icon(Icons.calendar_today, size: 16, color: AppColors.textDim),
                      const SizedBox(width: 10),
                      Text(
                        _dataHora != null
                            ? DateFormat('dd/MM/yyyy HH:mm').format(_dataHora!)
                            : 'Data e horário de saída',
                        style: TextStyle(
                          color: _dataHora != null ? AppColors.textPrimary : AppColors.textDim,
                          fontSize: 13,
                        ),
                      ),
                    ],
                  ),
                ),
              ),
              const SizedBox(height: 14),
              Row(
                children: [
                  Expanded(
                    child: TextField(
                      controller: _vagasController,
                      keyboardType: TextInputType.number,
                      style: const TextStyle(color: AppColors.textPrimary),
                      decoration: const InputDecoration(hintText: 'Vagas'),
                    ),
                  ),
                  const SizedBox(width: 12),
                  Expanded(
                    flex: 2,
                    child: Row(
                      children: [
                        Expanded(child: _tipoButton('Individual', TipoEvento.individual)),
                        const SizedBox(width: 8),
                        Expanded(child: _tipoButton('Grupo', TipoEvento.grupo)),
                      ],
                    ),
                  ),
                ],
              ),
              const SizedBox(height: 24),
              SizedBox(
                width: double.infinity,
                child: ElevatedButton(
                  onPressed: _salvando ? null : _salvar,
                  child: _salvando
                      ? const SizedBox(
                          height: 18,
                          width: 18,
                          child: CircularProgressIndicator(strokeWidth: 2, color: Colors.white),
                        )
                      : const Text('Criar Expedição'),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
