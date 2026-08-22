"""
Popula o banco com dados de demonstração para o TrailUp.

Uso (com MySQL rodando em localhost:3307):
    cd backend
    .devenv/state/venv/bin/python seed_demo.py

Credenciais demo criadas (senha: demo123):
    ana@trailup.demo
    bruno@trailup.demo
    joao@trailup.demo

O usuário já existente no banco é preservado.
"""
import datetime
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

os.environ.setdefault(
    "DATABASE_URL", "mysql+pymysql://root:@127.0.0.1:3307/trilhas_db"
)

from app import create_app
from extensions import db
from models.usuario_model import Usuario
from models.trilha_model import Trilha
from models.avaliacao_model import Avaliacao
from models.favorito_model import Favorito
from models.checkpoint_model import Checkpoint
from models.foto_model import Foto
from models.mapa_offline_model import MapaOffline
from models.evento_model import Evento, EventoTrilha, ParticipanteEvento
from models.notificacao_model import Notificacao
from models.historico_model import HistoricoTrilha, RegistroRealizado
from services.trilha_service import TrilhaService
from utils.auth import hash_senha

DEMO_SENHA = "demo123"

TRILHAS = [
    {
        "nome": "Trilha do Poço Preto",
        "localizacao": "Petrópolis, RJ",
        "distancia": 4.5,
        "duracao": 90,
        "dificuldade": "FACIL",
        "descricao": "Trilha leve pela mata atlântica com poço natural no final. Ideal para iniciantes.",
        "imagemUrl": "https://images.unsplash.com/photo-1441974231531-c6227db76b6e?w=800",
        "checkpoints": [
            (-22.3841, -43.1682),
            (-22.3835, -43.1670),
            (-22.3828, -43.1658),
            (-22.3820, -43.1645),
        ],
    },
    {
        "nome": "Morro da Urca",
        "localizacao": "Rio de Janeiro, RJ",
        "distancia": 3.2,
        "duracao": 75,
        "dificuldade": "MODERADA",
        "descricao": "Subida clássica com vista panorâmica da Zona Sul e Pão de Açúcar.",
        "imagemUrl": "https://images.unsplash.com/photo-1483728642387-6c3bdd6c93e5?w=800",
        "checkpoints": [
            (-22.9550, -43.1635),
            (-22.9542, -43.1628),
            (-22.9535, -43.1620),
            (-22.9528, -43.1612),
            (-22.9520, -43.1605),
        ],
    },
    {
        "nome": "Pico da Bandeira",
        "localizacao": "Alto Caparaó, MG",
        "distancia": 14.0,
        "duracao": 480,
        "dificuldade": "DIFICIL",
        "descricao": "Terceiro ponto mais alto do Brasil. Trilha longa, fria e exigente — leve equipamento completo.",
        "imagemUrl": "https://images.unsplash.com/photo-1464822759844-d150baec0134?w=800",
        "checkpoints": [
            (-20.4380, -41.7970),
            (-20.4370, -41.7960),
            (-20.4355, -41.7945),
            (-20.4340, -41.7930),
            (-20.4325, -41.7915),
            (-20.4310, -41.7900),
        ],
    },
    {
        "nome": "Cachoeira do Segredo",
        "localizacao": "São Thomé das Letras, MG",
        "distancia": 8.0,
        "duracao": 180,
        "dificuldade": "MODERADA",
        "descricao": "Caminhada até uma das cachoeiras mais bonitas de Minas, com trecho de pedras escorregadias.",
        "imagemUrl": "https://images.unsplash.com/photo-1432407692634-6434c2260c24?w=800",
        "checkpoints": [
            (-21.7210, -44.9850),
            (-21.7200, -44.9840),
            (-21.7190, -44.9830),
            (-21.7180, -44.9820),
        ],
    },
    {
        "nome": "Pedra Bonita",
        "localizacao": "São Conrado, RJ",
        "distancia": 6.0,
        "duracao": 150,
        "dificuldade": "MODERADA",
        "descricao": "Trilha popular para voo livre e mirante sobre a praia de São Conrado e Rocinha.",
        "imagemUrl": "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=800",
        "checkpoints": [
            (-22.9880, -43.2850),
            (-22.9870, -43.2840),
            (-22.9860, -43.2830),
            (-22.9850, -43.2820),
        ],
    },
    {
        "nome": "Trilha das 7 Cachoeiras",
        "localizacao": "Bonito, MS",
        "distancia": 5.0,
        "duracao": 120,
        "dificuldade": "FACIL",
        "descricao": "Percurso plano e sombreado passando por sete quedas d'água cristalinas.",
        "imagemUrl": "https://images.unsplash.com/photo-1470071459604-3b5ec3a7fe05?w=800",
        "checkpoints": [
            (-21.1260, -56.4810),
            (-21.1250, -56.4800),
            (-21.1240, -56.4790),
            (-21.1230, -56.4780),
            (-21.1220, -56.4770),
        ],
    },
]

USUARIOS_DEMO = [
    {"nome": "Ana Trilheira", "email": "ana@trailup.demo"},
    {"nome": "Bruno Guia", "email": "bruno@trailup.demo"},
    {"nome": "João Silva", "email": "joao@trailup.demo"},
]


def _get_or_create_user(nome, email):
    existente = Usuario.query.filter_by(email=email).first()
    if existente:
        return existente
    usuario = Usuario(
        nome=nome,
        email=email,
        senha=hash_senha(DEMO_SENHA),
        dataCadastro=datetime.date.today(),
    )
    db.session.add(usuario)
    db.session.commit()
    return usuario


def _criar_trilha(dados):
    existente = Trilha.query.filter_by(nome=dados["nome"]).first()
    if existente:
        return existente

    tempo = TrilhaService.calcular_tempo_estimado_min(dados["distancia"], dados["dificuldade"])
    trilha = Trilha(
        nome=dados["nome"],
        localizacao=dados["localizacao"],
        distancia=dados["distancia"],
        duracao=dados["duracao"],
        dificuldade=dados["dificuldade"],
        descricao=dados["descricao"],
        imagemUrl=dados.get("imagemUrl"),
        tempoEstimadoMin=tempo,
    )
    db.session.add(trilha)
    db.session.commit()

    base = datetime.datetime.utcnow() - datetime.timedelta(hours=2)
    for i, (lat, lng) in enumerate(dados.get("checkpoints", [])):
        db.session.add(
            Checkpoint(
                latitude=lat,
                longitude=lng,
                horario=base + datetime.timedelta(minutes=20 * i),
                idTrilha=trilha.idTrilha,
            )
        )

    db.session.add(
        MapaOffline(
            arquivoUrl=f"/offline_maps/trilha_{trilha.idTrilha}.map",
            tamanhoArquivo=round(dados["distancia"] * 1.8, 1),
            idTrilha=trilha.idTrilha,
        )
    )

    db.session.add(
        Foto(
            url=dados.get("imagemUrl", ""),
            legenda=f"Vista da {dados['nome']}",
            idTrilha=trilha.idTrilha,
        )
    )

    db.session.commit()
    return trilha


def seed():
    app = create_app()
    with app.app_context():
        if Trilha.query.count() >= len(TRILHAS):
            print("Demo já parece populada (trilhas existentes). Pulando inserção.")
            return

        usuarios = {}
        for u in USUARIOS_DEMO:
            user = _get_or_create_user(u["nome"], u["email"])
            usuarios[u["email"]] = user

        felipe = Usuario.query.filter_by(email="felipecleite13@gmail.com").first()
        if felipe:
            usuarios["felipe"] = felipe

        trilhas = [_criar_trilha(t) for t in TRILHAS]
        ana = usuarios["ana@trailup.demo"]
        bruno = usuarios["bruno@trailup.demo"]
        joao = usuarios["joao@trailup.demo"]

        avaliacoes = [
            (ana, trilhas[0], 5, "Poço Preto é perfeita para levar a família!"),
            (joao, trilhas[0], 4, "Boa para iniciantes, água gelada no final."),
            (ana, trilhas[1], 5, "Vista incrível do Rio, vale cada passo."),
            (bruno, trilhas[1], 4, "Fica lotada no fim de semana, chegue cedo."),
            (joao, trilhas[2], 5, "Desafiadora mas recompensadora. Leve agasalho!"),
            (bruno, trilhas[2], 5, "Experiência única ver o nascer do sol no topo."),
            (ana, trilhas[3], 4, "Cachoeira linda, cuidado com as pedras molhadas."),
            (joao, trilhas[4], 5, "Melhor ponto para fotos da cidade."),
            (ana, trilhas[5], 5, "Águas cristalinas, trilha bem sinalizada."),
        ]
        for usuario, trilha, nota, comentario in avaliacoes:
            if not Avaliacao.query.filter_by(idUsuario=usuario.idUsuario, idTrilha=trilha.idTrilha).first():
                db.session.add(
                    Avaliacao(
                        nota=nota,
                        comentario=comentario,
                        data=datetime.date.today() - datetime.timedelta(days=nota),
                        idUsuario=usuario.idUsuario,
                        idTrilha=trilha.idTrilha,
                    )
                )

        favoritos = [
            (ana, trilhas[0]),
            (ana, trilhas[1]),
            (joao, trilhas[2]),
            (joao, trilhas[4]),
            (bruno, trilhas[3]),
        ]
        if felipe:
            favoritos.append((felipe, trilhas[0]))
            favoritos.append((felipe, trilhas[5]))

        for usuario, trilha in favoritos:
            if not Favorito.query.filter_by(idUsuario=usuario.idUsuario, idTrilha=trilha.idTrilha).first():
                db.session.add(
                    Favorito(
                        dataSalvo=datetime.date.today(),
                        idUsuario=usuario.idUsuario,
                        idTrilha=trilha.idTrilha,
                    )
                )

        amanha = datetime.date.today() + datetime.timedelta(days=1)
        depois = datetime.date.today() + datetime.timedelta(days=3)

        eventos_dados = [
            {
                "titulo": "Nascer do sol no Pico",
                "descricao": "Saída madrugada para ver o sol no Pico da Bandeira.",
                "data": depois,
                "horarioSaida": datetime.datetime.combine(depois, datetime.time(3, 0)),
                "vagas": 8,
                "tipo": "GRUPO",
                "latitude": -20.4310,
                "longitude": -41.7900,
                "criador": bruno,
                "trilhas": [trilhas[2]],
                "participantes": [ana, joao],
            },
            {
                "titulo": "Urca no fim de tarde",
                "descricao": "Grupo para subir o Morro da Urca e ver o pôr do sol.",
                "data": amanha,
                "horarioSaida": datetime.datetime.combine(amanha, datetime.time(16, 30)),
                "vagas": 10,
                "tipo": "GRUPO",
                "latitude": -22.9520,
                "longitude": -43.1605,
                "criador": ana,
                "trilhas": [trilhas[1]],
                "participantes": [bruno],
            },
            {
                "titulo": "Bonito: 7 Cachoeiras",
                "descricao": "Expedição guiada pelas cachoeiras de Bonito.",
                "data": depois,
                "horarioSaida": datetime.datetime.combine(depois, datetime.time(8, 0)),
                "vagas": 6,
                "tipo": "GRUPO",
                "latitude": -21.1220,
                "longitude": -56.4770,
                "criador": joao,
                "trilhas": [trilhas[5]],
                "participantes": [ana],
            },
        ]

        eventos_criados = []
        for ev in eventos_dados:
            if Evento.query.filter_by(titulo=ev["titulo"]).first():
                continue
            evento = Evento(
                titulo=ev["titulo"],
                descricao=ev["descricao"],
                data=ev["data"],
                horarioSaida=ev["horarioSaida"],
                imediata=False,
                vagas=ev["vagas"],
                tipo=ev["tipo"],
                latitude=ev["latitude"],
                longitude=ev["longitude"],
                idCriador=ev["criador"].idUsuario,
            )
            db.session.add(evento)
            db.session.flush()

            for trilha in ev["trilhas"]:
                db.session.add(EventoTrilha(idEvento=evento.idEvento, idTrilha=trilha.idTrilha))

            db.session.add(
                ParticipanteEvento(idUsuario=ev["criador"].idUsuario, idEvento=evento.idEvento)
            )
            for p in ev["participantes"]:
                db.session.add(
                    ParticipanteEvento(idUsuario=p.idUsuario, idEvento=evento.idEvento)
                )

            eventos_criados.append(evento)

        historico_dados = [
            (joao, trilhas[0], 85.0, 5, None),
            (ana, trilhas[1], 70.0, 5, None),
            (bruno, trilhas[2], 420.0, 5, None),
        ]
        if felipe:
            historico_dados.append((felipe, trilhas[5], 110.0, 4, None))

        for usuario, trilha, tempo, aval_pessoal, id_evento in historico_dados:
            if HistoricoTrilha.query.filter_by(idUsuario=usuario.idUsuario, idTrilha=trilha.idTrilha).first():
                continue
            historico = HistoricoTrilha(
                dataRealizacao=datetime.date.today() - datetime.timedelta(days=7),
                tempo=tempo,
                avaliacaoPessoal=aval_pessoal,
                idUsuario=usuario.idUsuario,
                idEvento=id_evento,
                idTrilha=trilha.idTrilha,
            )
            db.session.add(historico)
            db.session.flush()

            cps = trilha.idTrilha and Checkpoint.query.filter_by(idTrilha=trilha.idTrilha).limit(2).all()
            for cp in cps or []:
                db.session.add(
                    RegistroRealizado(
                        latitude=cp.latitude,
                        longitude=cp.longitude,
                        horario=datetime.datetime.utcnow(),
                        observacao="Checkpoint registrado durante a trilha",
                        idHistorico=historico.idHistorico,
                    )
                )

        notificacoes = [
            (ana, "Sua expedição 'Urca no fim de tarde' tem 1 vaga restante!", eventos_criados[1] if len(eventos_criados) > 1 else None),
            (joao, "Bruno entrou na sua expedição 'Bonito: 7 Cachoeiras'.", eventos_criados[2] if len(eventos_criados) > 2 else None),
            (bruno, "Lembrete: Nascer do sol no Pico em 3 dias. Confira o checklist!", eventos_criados[0] if eventos_criados else None),
        ]
        if felipe:
            notificacoes.append((felipe, "Bem-vindo ao TrailUp! Explore trilhas perto de você.", None))

        for usuario, mensagem, evento in notificacoes:
            db.session.add(
                Notificacao(
                    mensagem=mensagem,
                    dataEnvio=datetime.datetime.utcnow(),
                    lida=False,
                    idUsuario=usuario.idUsuario,
                    idEvento=evento.idEvento if evento else None,
                )
            )

        db.session.commit()

        print("\n=== Demo data inserida com sucesso ===")
        print(f"  Trilhas:      {Trilha.query.count()}")
        print(f"  Usuários:     {Usuario.query.count()}")
        print(f"  Avaliações:   {Avaliacao.query.count()}")
        print(f"  Favoritos:    {Favorito.query.count()}")
        print(f"  Checkpoints:  {Checkpoint.query.count()}")
        print(f"  Eventos:      {Evento.query.count()}")
        print(f"  Histórico:    {HistoricoTrilha.query.count()}")
        print(f"  Notificações: {Notificacao.query.count()}")
        print("\nContas demo (senha: demo123):")
        for u in USUARIOS_DEMO:
            print(f"  - {u['email']}")
        if felipe:
            print(f"  - {felipe.email} (conta existente, senha original preservada)")


if __name__ == "__main__":
    seed()
