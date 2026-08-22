import 'package:flutter/material.dart';
import 'package:intl/intl.dart';
import '../../core/theme/app_theme.dart';
import '../../models/usuario.dart';
import '../../models/historico_trilha.dart';
import '../../models/notificacao.dart';
import '../../services/auth_service.dart';
import '../../services/historico_service.dart';
import '../../services/notificacao_service.dart';
import '../splash/splash_screen.dart';

class ProfileScreen extends StatefulWidget {
  final Usuario usuario;
  const ProfileScreen({super.key, required this.usuario});

  @override
  State<ProfileScreen> createState() => _ProfileScreenState();
}

class _ProfileScreenState extends State<ProfileScreen> {
  late Usuario _usuario;
  late Future<List<HistoricoTrilha>> _historicoFuture;
  late Future<List<Notificacao>> _notificacoesFuture;

  @override
  void initState() {
    super.initState();
    _usuario = widget.usuario;
    _carregar();
  }

  void _carregar() {
    if (_usuario.idUsuario != null) {
      _historicoFuture = HistoricoService.listarPorUsuario(_usuario.idUsuario!);
      _notificacoesFuture = NotificacaoService.listar(_usuario.idUsuario!);
    } else {
      _historicoFuture = Future.value([]);
      _notificacoesFuture = Future.value([]);
    }
  }

  void _abrirEdicao() {
    final nomeController = TextEditingController(text: _usuario.nome);
    showDialog(
      context: context,
      builder: (ctx) => AlertDialog(
        backgroundColor: AppColors.bgCard,
        title: const Text('Editar perfil', style: TextStyle(color: AppColors.textPrimary)),
        content: TextField(
          controller: nomeController,
          style: const TextStyle(color: AppColors.textPrimary),
          decoration: const InputDecoration(hintText: 'Nome'),
        ),
        actions: [
          TextButton(onPressed: () => Navigator.pop(ctx), child: const Text('Cancelar')),
          ElevatedButton(
            onPressed: () async {
              final atualizado =
                  await AuthService.atualizarPerfil(_usuario.copyWith(nome: nomeController.text.trim()));
              setState(() => _usuario = atualizado);
              if (ctx.mounted) Navigator.pop(ctx);
            },
            child: const Text('Salvar'),
          ),
        ],
      ),
    );
  }

  void _sair() {
    AuthService.logout();
    Navigator.pushAndRemoveUntil(
      context,
      MaterialPageRoute(builder: (_) => const SplashScreen()),
      (route) => false,
    );
  }

  String _iniciais(String nome) {
    final partes = nome.trim().split(' ').where((p) => p.isNotEmpty).toList();
    if (partes.isEmpty) return '?';
    if (partes.length == 1) return partes[0].substring(0, 1).toUpperCase();
    return (partes.first.substring(0, 1) + partes.last.substring(0, 1)).toUpperCase();
  }

  @override
  Widget build(BuildContext context) {
    return SafeArea(
      child: ListView(
        padding: const EdgeInsets.fromLTRB(24, 24, 24, 100),
        children: [
          Center(
            child: Column(
              children: [
                CircleAvatar(
                  radius: 44,
                  backgroundColor: AppColors.bgCard,
                  backgroundImage: _usuario.fotoPerfil != null ? NetworkImage(_usuario.fotoPerfil!) : null,
                  child: _usuario.fotoPerfil == null
                      ? Text(
                          _iniciais(_usuario.nome),
                          style: const TextStyle(
                              color: AppColors.greenLight, fontSize: 28, fontWeight: FontWeight.bold),
                        )
                      : null,
                ),
                const SizedBox(height: 12),
                Text(_usuario.nome,
                    style: const TextStyle(color: AppColors.textPrimary, fontSize: 20, fontWeight: FontWeight.bold)),
                Text(_usuario.email, style: const TextStyle(color: AppColors.textDim, fontSize: 13)),
                const SizedBox(height: 16),
                OutlinedButton.icon(
                  onPressed: _abrirEdicao,
                  style: OutlinedButton.styleFrom(backgroundColor: AppColors.bgCard, side: BorderSide.none),
                  icon: const Icon(Icons.edit, size: 16, color: AppColors.greenLight),
                  label: const Text('Editar perfil', style: TextStyle(color: AppColors.greenLight)),
                ),
              ],
            ),
          ),
          const SizedBox(height: 32),
          const Text('Histórico de Trilhas',
              style: TextStyle(color: AppColors.textPrimary, fontSize: 15, fontWeight: FontWeight.bold)),
          const SizedBox(height: 12),
          FutureBuilder<List<HistoricoTrilha>>(
            future: _historicoFuture,
            builder: (context, snapshot) {
              if (snapshot.connectionState == ConnectionState.waiting) {
                return const Padding(
                  padding: EdgeInsets.symmetric(vertical: 16),
                  child: Center(child: CircularProgressIndicator(color: AppColors.greenLight)),
                );
              }
              final historico = snapshot.data ?? [];
              if (historico.isEmpty) {
                return const Text('Nenhuma trilha concluída ainda.',
                    style: TextStyle(color: AppColors.textDim, fontSize: 12));
              }
              return Column(
                children: historico.map((h) {
                  return Container(
                    margin: const EdgeInsets.only(bottom: 10),
                    padding: const EdgeInsets.all(14),
                    decoration: BoxDecoration(color: AppColors.bgCard, borderRadius: BorderRadius.circular(12)),
                    child: Row(
                      children: [
                        const Icon(Icons.check_circle, color: AppColors.greenLight, size: 20),
                        const SizedBox(width: 12),
                        Expanded(
                          child: Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              Text(
                                h.nomeTrilha ?? 'Trilha #${h.idTrilha}',
                                style: const TextStyle(
                                    color: AppColors.textPrimary, fontWeight: FontWeight.bold, fontSize: 13),
                              ),
                              Text(
                                h.dataRealizacao != null ? DateFormat('dd/MM/yyyy').format(h.dataRealizacao!) : '--',
                                style: const TextStyle(color: AppColors.textDim, fontSize: 11),
                              ),
                              if (h.tempo != null)
                                Text(
                                  'Tempo: ${h.tempo!.round()} min',
                                  style: const TextStyle(color: AppColors.textDim, fontSize: 10),
                                ),
                            ],
                          ),
                        ),
                        if (h.avaliacaoPessoal != null)
                          Row(
                            children: List.generate(
                              5,
                              (i) => Icon(
                                i < h.avaliacaoPessoal! ? Icons.star : Icons.star_border,
                                size: 12,
                                color: AppColors.amber,
                              ),
                            ),
                          ),
                      ],
                    ),
                  );
                }).toList(),
              );
            },
          ),
          const SizedBox(height: 32),
          const Text('Notificações',
              style: TextStyle(color: AppColors.textPrimary, fontSize: 15, fontWeight: FontWeight.bold)),
          const SizedBox(height: 12),
          FutureBuilder<List<Notificacao>>(
            future: _notificacoesFuture,
            builder: (context, snapshot) {
              if (snapshot.connectionState == ConnectionState.waiting) {
                return const Padding(
                  padding: EdgeInsets.symmetric(vertical: 16),
                  child: Center(child: CircularProgressIndicator(color: AppColors.greenLight)),
                );
              }
              final notificacoes = snapshot.data ?? [];
              if (notificacoes.isEmpty) {
                return const Text('Sem notificações no momento.',
                    style: TextStyle(color: AppColors.textDim, fontSize: 12));
              }
              return Column(
                children: notificacoes.map((n) {
                  return Container(
                    margin: const EdgeInsets.only(bottom: 8),
                    padding: const EdgeInsets.all(12),
                    decoration: BoxDecoration(
                      color: n.lida ? AppColors.bgCard : AppColors.green.withOpacity(0.12),
                      borderRadius: BorderRadius.circular(10),
                    ),
                    child: Row(
                      children: [
                        Icon(
                          n.lida ? Icons.notifications_none : Icons.notifications_active,
                          size: 16,
                          color: n.lida ? AppColors.textDim : AppColors.greenLight,
                        ),
                        const SizedBox(width: 10),
                        Expanded(
                          child: Text(n.mensagem, style: const TextStyle(color: AppColors.textPrimary, fontSize: 12)),
                        ),
                      ],
                    ),
                  );
                }).toList(),
              );
            },
          ),
          const SizedBox(height: 32),
          SizedBox(
            width: double.infinity,
            child: OutlinedButton.icon(
              onPressed: _sair,
              style: OutlinedButton.styleFrom(backgroundColor: AppColors.bgCard, side: BorderSide.none),
              icon: const Icon(Icons.logout, size: 18, color: AppColors.red),
              label: const Text('Sair da conta', style: TextStyle(color: AppColors.red)),
            ),
          ),
        ],
      ),
    );
  }
}
