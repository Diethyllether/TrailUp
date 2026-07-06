import 'package:flutter/material.dart';
import 'package:intl/intl.dart';
import '../core/theme/app_theme.dart';
import '../models/evento.dart';

class EventoCard extends StatelessWidget {
  final Evento evento;
  final VoidCallback? onParticipar;
  final VoidCallback? onReportar;

  const EventoCard({super.key, required this.evento, this.onParticipar, this.onReportar});

  @override
  Widget build(BuildContext context) {
    final accent = AppColors.difficultyColor(evento.dificuldadeTrilha);
    return Container(
      margin: const EdgeInsets.only(bottom: 12),
      decoration: BoxDecoration(color: AppColors.bgCard, borderRadius: BorderRadius.circular(14)),
      clipBehavior: Clip.antiAlias,
      child: IntrinsicHeight(
        child: Row(
          children: [
            Container(width: 4, color: accent),
            Expanded(
              child: Padding(
                padding: const EdgeInsets.all(14),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Row(
                      children: [
                        Expanded(
                          child: Text(
                            evento.titulo,
                            style: const TextStyle(
                                color: AppColors.textPrimary, fontWeight: FontWeight.bold, fontSize: 14),
                          ),
                        ),
                        if (onReportar != null)
                          GestureDetector(
                            onTap: onReportar,
                            child: const Icon(Icons.flag_outlined, size: 16, color: AppColors.textDim),
                          ),
                      ],
                    ),
                    const SizedBox(height: 6),
                    Text(
                      '👤 ${evento.nomeCriador ?? 'Líder'}  •  '
                      '${evento.data != null ? DateFormat('dd/MM HH:mm').format(evento.data!) : '--'}',
                      style: const TextStyle(color: AppColors.textDim, fontSize: 11),
                    ),
                    const SizedBox(height: 10),
                    Row(
                      children: [
                        Container(
                          padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
                          decoration:
                              BoxDecoration(color: AppColors.bgMid, borderRadius: BorderRadius.circular(10)),
                          child: Text('${evento.vagasFormatadas} vagas',
                              style: const TextStyle(color: AppColors.textDim, fontSize: 10)),
                        ),
                        const Spacer(),
                        ElevatedButton(
                          onPressed: onParticipar,
                          style: ElevatedButton.styleFrom(
                            padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
                            minimumSize: Size.zero,
                            tapTargetSize: MaterialTapTargetSize.shrinkWrap,
                          ),
                          child: const Text('Entrar', style: TextStyle(fontSize: 12)),
                        ),
                      ],
                    ),
                  ],
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
