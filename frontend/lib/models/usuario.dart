class Usuario {
  final int? idUsuario;
  final String nome;
  final String email;
  final String? senha;
  final String? fotoPerfil;
  final DateTime? dataCadastro;

  Usuario({
    this.idUsuario,
    required this.nome,
    required this.email,
    this.senha,
    this.fotoPerfil,
    this.dataCadastro,
  });

  factory Usuario.fromJson(Map<String, dynamic> json) {
    return Usuario(
      idUsuario: json['idUsuario'] as int?,
      nome: json['nome'] as String,
      email: json['email'] as String,
      fotoPerfil: json['fotoPerfil'] as String?,
      dataCadastro:
          json['dataCadastro'] != null ? DateTime.tryParse(json['dataCadastro']) : null,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      if (idUsuario != null) 'idUsuario': idUsuario,
      'nome': nome,
      'email': email,
      if (senha != null) 'senha': senha,
      if (fotoPerfil != null) 'fotoPerfil': fotoPerfil,
    };
  }

  Usuario copyWith({String? nome, String? email, String? fotoPerfil}) {
    return Usuario(
      idUsuario: idUsuario,
      nome: nome ?? this.nome,
      email: email ?? this.email,
      fotoPerfil: fotoPerfil ?? this.fotoPerfil,
      dataCadastro: dataCadastro,
    );
  }
}
