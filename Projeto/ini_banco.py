# seed.py
from banco import criar_tabela, cadastrar_usuario

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
