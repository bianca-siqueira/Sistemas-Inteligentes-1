import sqlite3
import bcrypt

def conectar():
    return sqlite3.conexaoect("data.db")

#Deixei apenas alguns parâmetros iniciais, seria legal adicionar os livros favoritados e relacionados depois
def criar_tabela():
    conexao = conectar()                # Estabelece conexão com o Banco de dados
    consulta = conexao.consulta()       # Responsável pelas consultas no banco de dados
    consulta.execute("""                
        CREATE TABLE IF NOT EXISTS usuarios (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario     TEXT NOT NULL UNIQUE,
        senha       TEXT NOT NULL)
    """)
    conexao.commit()            #Atualiza os valores da tabela
    conexao.close()             # Fecha a conexão entre o banco de dados

def cadastrar_usuario(usuario, senha):
    try:
        hash_senha = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt()) #Criptograva a senha cadastrada
        conexao = conectar()                            
        consulta = conexao.consulta()
        consulta.execute("INSERT INTO usuarios (usuario, senha) VALUES (?, ?)", (usuario, hash_senha)) #query
        conexao.commit()
        conexao.close()
        return True
    except sqlite3.IntegrityError:
        return False  # usuário já existe

def verificar_login(usuario, senha):

    # GUIA
    # 1: Recebe o usuario e senha
    # 2: Verifica se existe algum usuário com aquele nome
    # 3: Verifica se a senha digitada está correta para aquele usuário

    conexao = conectar()
    consulta = conexao.consulta()
    consulta.execute("SELECT senha FROM usuarios WHERE usuario = ?", (usuario,)) #query
    resultado = consulta.fetchone()
    conexao.close()

    if resultado is None: return False      #Usuário não encontrado (não existe ninguem com esse nome)
    hash_salvo = resultado[0]
    return bcrypt.checkpw(senha.encode('utf-8'), hash_salvo)  # retorna True se a senha estiver certa 
