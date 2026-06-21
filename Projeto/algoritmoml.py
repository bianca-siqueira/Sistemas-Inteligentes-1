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
from surprise import SVD, Dataset, Reader

# 1: CARREGA TODAS AS AVALIAÇÕES
# 2: faz a fatoração de matrizes com base nas duas matrizes unidas (planilha+banco)

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
        print("Arquivo não encontrado!")

def avaliacoes_banco():
    conexao = conectar()
    df_banco = pd.read_sql_query("SELECT usuario, ISBN, nota FROM avaliacoes", conexao)
    conexao.close()

    df_banco.columns = ["User-ID","ISBN","Book-Rating"] #COlunas com mesmo nome do dataset
    return df_banco

def filtro(av):
    cont = av['ISBN'].value_counts()
    livros_validos = cont[cont >= 50].index
    av = av[av['ISBN'].isin(livros_validos)] #coloca apenas livros que possuem mais de x avaliações

    cont_usuarios = av['User-ID'].value_counts()
    usuarios_validos = cont_usuarios[cont_usuarios >= 5].index
    av = av[av['User-ID'].isin(usuarios_validos)] # Usuarios que possuem apenas mais de 20 avaliações
    return av

def recomendar():
    av = carregar_dataset()
    av = filtro(av)             #Pega apenas alguns dados pro meu pc conseguir rodar

    config  = Reader(rating_scale=(1,10)) # COnfiguração para identificar que Nota Minima : 1 e Nota Maxima : 10
    dados =   Dataset.load_from_df(av[['User-ID', 'ISBN', 'Book-Rating']], config) 
    treino = dados.build_full_trainset()
    modelo = SVD(n_factors=15, lr_all=0.0005, n_epochs=100, biased=False) # Configura o que o modelo precisa fazer
    modelo.fit(treino)  #Inicia o algoritmo com base nas configurações acima

    usuario_teste = "276725"
    livro_teste = "034545104X"
    
    previsao_final = modelo.predict(usuario_teste, livro_teste)
    
    # O '.est' extrai a nota estimada final calculada pelo modelo
    print(f"\n[Resultado] Nota prevista para o usuário {usuario_teste} no livro {livro_teste}: {previsao_final.est:.2f}")

recomendar()

#OBS: o meu notebook estava gastando muita memória para processar todos os livros, portanto, vou adicionar esse filtro, mas dá pra tirar depois 
    # para deixar ele rodando no bruto, mas vou filtrar os que possuem mais avaliações só para conseguir rodar
#OBS: Livros que não possuem avaliação não entraram no cálculo
#OBS: matriz_base possui valores 0 em algumas colunas pois alguns usuarios não leram alguns livros