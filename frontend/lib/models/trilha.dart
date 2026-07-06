import 'avaliacao.dart';
import 'foto.dart';

class Trilha {
  final int? idTrilha;
  final String nome;
  final String? localizacao;
  final double? distancia;
  final double? duracao;
  final String? dificuldade;
  final String? descricao;

  final double? avaliacaoMedia;
  final String? imagemCapa;
  final List<Avaliacao>? avaliacoes;
  final List<Foto>? fotos;

  Trilha({
    this.idTrilha,
    required this.nome,
    this.localizacao,
    this.distancia,
    this.duracao,
    this.dificuldade,
    this.descricao,
    this.avaliacaoMedia,
    this.imagemCapa,
    this.avaliacoes,
    this.fotos,
  });

  factory Trilha.fromJson(Map<String, dynamic> json) {
    return Trilha(
      idTrilha: json['idTrilha'] as int?,
      nome: json['nome'] as String,
      localizacao: json['localizacao'] as String?,
      distancia: (json['distancia'] as num?)?.toDouble(),
      duracao: (json['duracao'] as num?)?.toDouble(),
      dificuldade: json['dificuldade'] as String?,
      descricao: json['descricao'] as String?,
      avaliacaoMedia: (json['avaliacaoMedia'] as num?)?.toDouble(),
      imagemCapa: json['imagemUrl'] as String? ?? json['imagemCapa'] as String?,
      avaliacoes: json['avaliacoes'] != null
          ? (json['avaliacoes'] as List).map((e) => Avaliacao.fromJson(e)).toList()
          : null,
      fotos: json['fotos'] != null
          ? (json['fotos'] as List).map((e) => Foto.fromJson(e)).toList()
          : null,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      if (idTrilha != null) 'idTrilha': idTrilha,
      'nome': nome,
      'localizacao': localizacao,
      'distancia': distancia,
      'duracao': duracao,
      'dificuldade': dificuldade,
      'descricao': descricao,
    };
  }

  String get duracaoFormatada {
    if (duracao == null) return '--';
    final h = duracao! ~/ 60;
    final m = (duracao! % 60).toInt();
    if (h > 0) return '${h}h ${m}min';
    return '${m}min';
  }
}
