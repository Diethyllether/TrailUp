import 'package:flutter/material.dart';

import '../../models/usuario.dart';

/// Tela mantida apenas para compatibilidade com o aplicativo Flutter legado.
///
/// O produto TrailUp foi migrado para o frontend web Flask/Jinja2. As páginas
/// de trilha, incluindo mapa e rota, agora são renderizadas no navegador com
/// Google Maps. O aplicativo mobile não oferece mais download de mapas.
class TrilhaDetailScreen extends StatelessWidget {
  final int idTrilha;
  final Usuario usuario;

  const TrilhaDetailScreen({
    super.key,
    required this.idTrilha,
    required this.usuario,
  });

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('TrailUp')),
      body: Center(
        child: ConstrainedBox(
          constraints: const BoxConstraints(maxWidth: 460),
          child: Padding(
            padding: const EdgeInsets.all(24),
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                const Icon(Icons.public, size: 64),
                const SizedBox(height: 20),
                const Text(
                  'O TrailUp agora é web',
                  textAlign: TextAlign.center,
                  style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
                ),
                const SizedBox(height: 12),
                Text(
                  'A trilha #$idTrilha e seus mapas agora devem ser acessados pelo site do TrailUp. '
                  'O aplicativo Flutter foi descontinuado e não possui mais mapas offline.',
                  textAlign: TextAlign.center,
                ),
                const SizedBox(height: 20),
                FilledButton.icon(
                  onPressed: () => Navigator.of(context).pop(),
                  icon: const Icon(Icons.arrow_back),
                  label: const Text('Voltar'),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
