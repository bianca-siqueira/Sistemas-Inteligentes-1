import sqlite3
import bcrypt

def conectar():
    return sqlite3.connect("data.db")

def criar_tabela():
    conexao = conectar()
    consulta = conexao.cursor()

    consulta.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT NOT NULL UNIQUE,
            senha BLOB NOT NULL
        )
    """)
    conexao.commit()
    conexao.close()
def cadastrar_usuario(usuario, senha):
    try:
        hash_senha = bcrypt.hashpw(
            senha.encode('utf-8'),
            bcrypt.gensalt()
        )
        conexao = conectar()
        consulta = conexao.cursor()
        consulta.execute(
            "INSERT INTO usuarios (usuario, senha) VALUES (?, ?)",
            (usuario, hash_senha)
        )
        conexao.commit()
        conexao.close()
        return True

    except sqlite3.IntegrityError:
        return False

def verificar_login(usuario, senha):
    conexao = conectar()
    consulta = conexao.cursor()

    consulta.execute(
        "SELECT senha FROM usuarios WHERE usuario = ?",
        (usuario,)
    )

    resultado = consulta.fetchone()
    conexao.close()

    if resultado is None:
        return False

    hash_salvo = resultado[0]

    return bcrypt.checkpw(
        senha.encode('utf-8'),
        hash_salvo
    )
