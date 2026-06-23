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
    usuarios_validos = cont_usuarios[cont_usuarios >= 20].index
    av = av[av['User-ID'].isin(usuarios_validos)]
    return av
'''
def SVD(matriz_base):
    k = 100
    incremento = 0.00013
    erro_limite = 0.05
    iteracoes = 5000
    av = matriz_base.to_numpy()
    mascara = (av >0)
    av_validas = np.sum(mascara)

    x, f = av.shape[0], av.shape[1]
    u = np.random.rand(x,k)/np.sqrt(k)
    q = np.random.rand(k,f)/np.sqrt(k)

    cont,erro_atual,erro_emcelula = 0, float('inf'), float('inf')
    while erro_emcelula > erro_limite and cont < iteracoes:
        # l1, c1: l1cl1*l1*cl1 + l2*cl1
        palpite = np.dot(u,q)

        if np.isnan(palpite).any() or np.isinf(palpite).any():
            print("Gradiente começou a explodir, reduza o incremento")
            break

        matriz_erro = av - palpite
        matriz_erro = matriz_erro*mascara                
        erro_atual = np.sum(matriz_erro** 2)             #Soma de TODOS os erros para todos os usuários
        erro_emcelula = np.sqrt(erro_atual / av_validas) #média de erro para cada livro

        # Formula de erro: (Av_real - palpite)^2 => (Av_real - uxq)^2
        # Gradiente de u:  2*(Av_real-uxq)*(-q)         (Regra da Cadeia para descobrir u)
        # Gradiente de q:  2*(Av_real - uxq)((-u))      (Regra da Cadeia para descobrir q)
        u =  u - incremento*(-2*np.dot(matriz_erro, q.T))
        q = q - incremento*(-2*np.dot(u.T, matriz_erro))

        cont +=1
        if cont % 100 == 0:
            print(f"Época {cont} -> Erro Quadrático Total: {erro_atual:.4f}, Erro em celula: {erro_emcelula} ")

    print(f"Treinamento finalizado! Iterações : {cont}, Erro total: {erro_atual}, Erro em celula: {erro_emcelula}" )
    return u,q
'''

def recomendar():
    av = carregar_dataset()
    av = filtro(av)             #Pega apenas alguns dados pro meu pc conseguir rodar

    config  = Reader(rating_scale=(1,10)) # COnfiguração para identificar que Nota Minima : 1 e Nota Maxima : 10
    dados =   Dataset.load_from_df(av[['User-ID', 'ISBN', 'Book-Rating']], config) 
    treino = dados.build_full_trainset()
    modelo = SVD(n_factors=15, lr_all=0.0005, n_epochs=100, biased=False)
    modelo.fit(treino)
    #predicao = modelo.predict(usuario_teste, livro_teste)

'''
def recomendar():
    k = 100
    av = carregar_dataset()
    av = filtro(av)
    matriz_base = av.pivot(index="User-ID",columns="ISBN",values="Book-Rating").fillna(0) #Organiza Tabela base, coloca valores vazios onde não está preenchido (usuarios não leram)
    
    print("Matriz base criada!!")
    #u_treinado, q_treinado = SVD(matriz_base)
    reader = Reader(rating_scale(1,10))
    dados_surprise = Dataset.load_from_df(av[['User-ID', 'ISBN', 'Book-Rating']], reader)
    base_treino = dados_surprise.build_full_trainset()
    modelo = SVD(n_factors=15, lr_all=0.0005, epochs=100, biased=False)

    print("Treinando o modelo Funk-SVD pela biblioteca...")
    modelo.fit(base_treino)
    print("Treinamento concluído!")
    usuario_teste = "276725"
    livro_teste = "034545104X"
    
    predicao = modelo.predict(usuario_teste, livro_teste)
    print(f"\nNota prevista para {usuario_teste} no livro {livro_teste}: {predicao.est:.2f}")
'''
recomendar()

#OBS: o meu notebook estava gastando muita memória para processar todos os livros, portanto, vou adicionar esse filtro, mas dá pra tirar depois 
    # para deixar ele rodando no bruto, mas vou filtrar os que possuem mais avaliações só para conseguir rodar
#OBS: Livros que não possuem avaliação não entraram no cálculo
#OBS: matriz_base possui valores 0 em algumas colunas pois alguns usuarios não leram alguns livros