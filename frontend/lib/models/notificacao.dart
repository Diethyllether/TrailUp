class Notificacao {
  final int? idNotificacao;
  final String mensagem;
  final DateTime? dataEnvio;
  final bool lida;
  final int idUsuario;
  final int? idEvento;

  Notificacao({
    this.idNotificacao,
    required this.mensagem,
    this.dataEnvio,
    this.lida = false,
    required this.idUsuario,
    this.idEvento,
  });

  factory Notificacao.fromJson(Map<String, dynamic> json) {
    return Notificacao(
      idNotificacao: json['idNotificacao'] as int?,
      mensagem: json['mensagem'] as String,
      dataEnvio: json['dataEnvio'] != null ? DateTime.tryParse(json['dataEnvio']) : null,
      lida: json['lida'] as bool? ?? false,
      idUsuario: json['idUsuario'] as int,
      idEvento: json['idEvento'] as int?,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'mensagem': mensagem,
      'lida': lida,
      'idUsuario': idUsuario,
      if (idEvento != null) 'idEvento': idEvento,
    };
  }
}
