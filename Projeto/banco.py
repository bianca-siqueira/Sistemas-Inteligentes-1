import sqlite3
import bcrypt

def conectar():
    conexao = sqlite3.connect("data.db",timeout=10) # Adicionado Timeout para não dar "banco closed" 
    conexao.execute("PRAGMA journal_mode = WAL;") #Escrita e leitura simultanea
    conexao.execute("PRAGMA foreign_keys = ON;")
    return conexao

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
    consulta.execute("""
        CREATE TABLE IF NOT EXISTS avaliacoes (
            id      INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER NOT NULL,
            ISBN    TEXT NOT NULL,
            nota    INTEGER NOT NULL,
            FOREIGN KEY (usuario_id) REFERENCES usuarios (id))
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
        "SELECT id, senha FROM usuarios WHERE usuario = ?",
        (usuario,)
    )

    resultado = consulta.fetchone()
    conexao.close()

    if resultado is None:
        return False

    usuario_id = resultado[0]
    hash_salvo = resultado[1]

    if bcrypt.checkpw(senha.encode('utf-8'), hash_salvo):
        return usuario_id
    else:
        return None
    
def obter_user_id(username):
    conexao = conectar()
    consulta = conexao.cursor()
    consulta.execute("SELECT id FROM usuarios WHERE usuario = ?", (username,))
    resultado = consulta.fetchone()
    conexao.close()
    return resultado[0] if resultado else None

def adicionar_avaliacao(usuario_id,ISBN,nota):
    conexao = conectar()
    consulta = conexao.cursor()

    consulta.execute(
        "INSERT INTO avaliacoes (usuario_id, ISBN, nota) VALUES (?,?,?)",(usuario_id,ISBN,nota))
    conexao.commit()
    conexao.close()