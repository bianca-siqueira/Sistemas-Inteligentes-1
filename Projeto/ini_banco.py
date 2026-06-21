# seed.py
from banco import criar_tabela, cadastrar_usuario, adicionar_avaliacao, obter_user_id

criar_tabela()

usuarios_teste = [
    ("admin", "admin123"),
    ("Anna", "123456"),
    ("Bianca", "123456"),
    ("Lais", "123456"),
]

for usuario, senha in usuarios_teste:
    sucesso = cadastrar_usuario(usuario, senha)
    if sucesso:
        print(f"Usuário '{usuario}' criado com sucesso!")
    else:
        print(f"Usuário '{usuario}' já existe no banco.")
teste_avaliacao = [
    ("Anna", "0195153448", 8),
    ("Anna", "0374157065", 7),
    ("Anna", "0375705856", 5),
    ("Anna", "0440241413", 10),
    ("Anna", "1401201172", 2),
    ("Anna", "8486433193", 6),
    ("Anna", "1841721522", 3),
    ("Anna", "0553582909", 10),
    ("Anna", "0316769487", 9),
    ("Anna", "0446608653", 1)
]

for usuario, ISBN, nota in teste_avaliacao:
    try:
        usuario_id = obter_user_id(usuario)
        adicionar_avaliacao(usuario_id,ISBN,nota)
        print(f"Avaliacao cadastrada: {usuario}, {ISBN}, {nota}")
    except Exception as e:
        print(f"Erro!")
