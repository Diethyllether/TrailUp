class ChecklistItem {
  final String descricao;
  final bool obrigatorio;
  bool concluido;

  ChecklistItem({
    required this.descricao,
    required this.obrigatorio,
    this.concluido = false,
  });
}
