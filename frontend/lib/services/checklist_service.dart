import '../models/checklist_item.dart';
import '../models/trilha.dart';

class ChecklistService {
  ChecklistService._();

  static List<ChecklistItem> gerarParaTrilha(Trilha trilha) {
    final items = <ChecklistItem>[
      ChecklistItem(descricao: "Garrafa d'água", obrigatorio: true),
      ChecklistItem(descricao: 'Lanche leve', obrigatorio: true),
      ChecklistItem(descricao: 'Protetor solar', obrigatorio: true),
      ChecklistItem(descricao: 'Celular carregado', obrigatorio: true),
    ];

    final dif = trilha.dificuldade?.toLowerCase() ?? '';
    final distancia = trilha.distancia ?? 0;

    if (distancia >= 5 || dif.contains('moder')) {
      items.addAll([
        ChecklistItem(descricao: 'Bota de trilha', obrigatorio: true),
        ChecklistItem(descricao: 'Kit de primeiros socorros', obrigatorio: true),
        ChecklistItem(descricao: 'Repelente', obrigatorio: false),
      ]);
    }

    if (distancia >= 10 || dif.contains('difíc') || dif.contains('dificil')) {
      items.addAll([
        ChecklistItem(descricao: 'Bastões de caminhada', obrigatorio: false),
        ChecklistItem(descricao: 'Lanterna / headlamp', obrigatorio: true),
        ChecklistItem(descricao: 'Capa de chuva', obrigatorio: true),
        ChecklistItem(descricao: 'Agua extra (2L+)', obrigatorio: true),
      ]);
    }

    if (!(dif.contains('fác') || dif.contains('facil'))) {
      items.add(ChecklistItem(descricao: 'Mapa offline baixado', obrigatorio: true));
    }

    return items;
  }
}
