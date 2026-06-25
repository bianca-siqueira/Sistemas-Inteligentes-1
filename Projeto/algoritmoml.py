#Para o Algoritmo Principal temos:
# Histórico do Usuário 
# Classificar: gênero e nota (review)
#
# Caso seja a primeira vez do usuário: 
# Conta nova -> Gerar aleatório (pegar os top X melhores)
#
# 
#############################################################

# Função que faça o link do usuário com o histórico
#
# precisa: id, login, senha, livro cadastrado e a avaliação dele


#import pandas as pd 
#Lembrando que o caminho pode ser diferente!!
#df = pd.read_excel("/Content/dataset_final.xlsx")

#print(df.head())

#Usar modelo - Fatoração de Matrizes - deep learning


import pandas as pd #pip install openpyxl
import sqlite3
import numpy as np
from surprise.model_selection import train_test_split
from surprise import SVD, Dataset, Reader, accuracy

# 1: CARREGA TODAS AS AVALIAÇÕES
# 2: faz a fatoração de matrizes com base nas duas matrizes unidas (planilha+banco)

#Abre o dataset de forma GLOBAL, abrindo apenas 1 vez em todo o ciclo do aplicativo
try:
    df = pd.read_excel("Content/dataset_final.xlsx", engine="openpyxl",usecols=['ISBN', 'Book-Title', 'Image-URL-M'], dtype={'ISBN': str},dtype_backend="pyarrow")
except Exception as e:
    print("Erro ao carregar dataset!",e)
    df = None

def conectar():
    return sqlite3.connect("data.db")

# Carrega todos os datasets (banco+planilha) para usar como treino
def carregar_dataset():
    try:
        #df = pd.read_excel("Content/dataset_final.xlsx",dtype={'ISBN': str, 'Book-Rating': float})
        av_dataset = pd.read_csv("Content/ratings.csv",dtype={'User-ID': str, 'ISBN': str, 'Book-Rating': float},encoding='latin-1',sep=';')
        av_banco = avaliacoes_banco()
        av = pd.concat([av_dataset, av_banco], ignore_index=True) #
        av = av.dropna(subset=["User-ID", "ISBN", "Book-Rating"])
        av = av.drop_duplicates(subset=["User-ID", "ISBN"], keep="last")   #Mantem apenas as ultimas avaliações (retira duplicação pela ordem de empilhação da tabela) 

        return av
    
    except FileNotFoundError:
        raise FileNotFoundError("O arquivo 'Content/ratings.csv' não foi encontrado!")
def avaliacoes_banco():
    conexao = conectar()
    df_banco = pd.read_sql_query("SELECT usuario_id, ISBN, nota FROM avaliacoes", conexao)
    conexao.close()
    df_banco.columns = ["User-ID","ISBN","Book-Rating"] #COlunas com mesmo nome do dataset
    df_banco['User-ID'] = "app_" + df_banco['User-ID'].astype(str)
    return df_banco

def filtro(av):
    
    av_banco = avaliacoes_banco()
    livros_banco = av_banco['ISBN'].unique()
    usuarios_banco = av_banco['User-ID'].unique()

    cont = av['ISBN'].value_counts()
    livros_validos = cont[cont >= 50].index

    cont_usuarios = av['User-ID'].value_counts()
    usuarios_validos = cont_usuarios[cont_usuarios >= 5].index
    
    filtro_livro = av['ISBN'].isin(livros_validos) | av['ISBN'].isin(livros_banco)
    filtro_user = av['User-ID'].isin(usuarios_validos) | av['User-ID'].isin(usuarios_banco)

    av_filter = av[filtro_livro & filtro_user] # Usuarios que possuem apenas mais de 4 avaliações no dataset ou que estão no aplicativo
    return av_filter

def n_recomendacoes(usuario_id, av, modelo, n):

    livros_lidos = av[av['User-ID'] == usuario_id]['ISBN'].unique()   #encontra os livros que ele já leu e não recomenda
    print(f"Já li esses livros aqui: {livros_lidos}")
    
    todos_livros = av['ISBN'].unique()                               
    livros_nao_lidos = list(set(todos_livros) - set(livros_lidos))    # Retira os livros lidos do campo de livros gerais

    if len(livros_lidos) <= 3:                                      # Se o usuário não possuir mais de 2 avaliações, recomenda livros populares
        livros_populares = av['ISBN'].value_counts().head(n).index.tolist()
        return [(isbn, 10) for isbn in livros_populares]
    
    recomendacao = []
    livros_rec = set()

    for livro in livros_nao_lidos:          #Recomenda livros que não foram lidos e que a nota prevista foi alta
        livro_limp = str(livro).strip()
        if livro_limp in livros_rec:
            continue

        pred = modelo.predict(usuario_id,livro)
        recomendacao.append((livro,pred.est))
        livros_rec.add(livro_limp)

    recomendacao.sort(key=lambda x: x[1],reverse=True)
    return recomendacao[:n]

def retorna_url(isbn):
    try:
        isbn_str = str(isbn).strip().upper()
        URL = df[df['ISBN'] ==isbn_str]

        if not URL.empty:
            url_img = URL.iloc[0]['Image-URL-M']
            title = URL.iloc[0]['Book-Title']
            return url_img,title
        else: return None, "Titulo Desconhecido"
    
    except Exception as e:
        print("Erro ao abrir ao tentar pegar as capas dos livros!")

def recomendar(user_id,user):
    av = carregar_dataset()
    av = filtro(av)             #Pega apenas alguns dados pro meu pc conseguir rodar
    usuario_alvo = f"app_{user_id}"

    config  = Reader(rating_scale=(1,10)) # COnfiguração para identificar que Nota Minima : 1 e Nota Maxima : 10
    dados =   Dataset.load_from_df(av[['User-ID', 'ISBN', 'Book-Rating']], config) 
    #Test_size: porcentagem dos dados que vão para o teste
    #   - Dados do teste ficam escondidos para usar como comparação no final
    #Random_state: Emabaralha os dados pra não cortar apenas um grupo específico
    treino, teste = train_test_split(dados,test_size=0.2,random_state=42) 
    
    modelo = SVD(n_factors=15, lr_all=0.0005, n_epochs=100, biased=True) # Configura o que o modelo precisa fazer
    modelo.fit(treino)  #Inicia o algoritmo com base nas configurações acima
    predicao = modelo.test(teste) #Lista de Objetos que guarda as notas que são calculadas

    sugestao_ini = n_recomendacoes(usuario_alvo,av,modelo,10)
    sugestao = []

    #Adiciona o URL e o TItulo das obras recomendadas
    for isbn,nota in sugestao_ini:
        url,title  = retorna_url(isbn)
        sugestao.append((isbn,nota,url,title))

    Rmse = accuracy.rmse(predicao, verbose=False)
    mse = accuracy.mae(predicao, verbose=False)
    print(f"VALOR RMSE MÉDIO:{Rmse} \n")
    print(f"VALOR MAE MÉDIO:{mse} \n")

    print(f" ========== TOP 10 LIVROS PARA {user} ==========")
    for indice, (isbn, nota_prevista,url,title) in enumerate(sugestao, start=1):
        print(f"{indice}º Lugar - Título: {title} | ISBN: {isbn} | Nota Prevista: {nota_prevista:.2f}")
    return sugestao

#OBS: Livros que não possuem avaliação não entraram no cálculo
#OBS: matriz_base possui valores 0 em algumas colunas pois alguns usuarios não leram alguns livros
