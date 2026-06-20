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

# Colunas: Livros
# Linhas:  Usuarios
# Valor l-c: Avaliação do usuario

#       2 Colunas iguais: filmes parecidos
#       (1)(2) + (2)(2) = (3)(2) uma pessoa que gosta das duas categorias
#       (all)(2) e (all)(3) = filmes parecidos

# SUB MATRIZES:
# R = P * Q^t
#   R: matriz original: usuarios(m) x livros(n)
#   P: m * k (gostos ocultos, dimensões terinadas)
#   Q: n*k   (vetor)
#   nota usuario: produto escalar: r = (p *q) + media_glob



#   
#Matriz geral é resultado de um produto de duas matrizes
#   Matriz 1 - Usuarios: 1 se gosta de tal genero, 0 se não gosta de tal genero
#       - O machine Learning chuta valores iniciais para se aproximar da nota do usuario (0.8, 0.2 e etc, maximo 1)
#   Matriz 2: Valor dos generos em cada livro
#       - O machine learning chuta valores iniciais (maximo 10 ou 5 (Estrelas))
# OBS: aumenta os valores dos dois aos poucos até encontrar uma correspondencia com a avaliação original
#       - Erro:  determinar quanto de diferença o algoritmo aceita ou não (troca)
#           - EXEMPLO: avaliação oficial: 3
#           - l-c 1.44, então o erro é: (3-1.44)^2 + todas as coluunas
# Avaliação = quanto da "categoria" tem o que usuario gosta
# Gosta de mais de uma categoria: soma a ponderação
# Linhas iguais podem acontecer se duas pessoas tiverem a mesma preferência

import pandas as pd #pip install openpyxl
import sqlite3

# 1: CARREGA TODAS AS AVALIAÇÕES
# 2: faz a fatoração de matrizes


# Carrega a avaliação de TODOS os usuários para treinar a recomendação
def carregar_dataset():
    try:
        df = pd.read_excel("Content/dataset_final.xlsx")
        av = pd.real("Content/ratings.csv")
        print(av.head(5))
        return df, av
    except FileNotFoundError:
        print("Arquivonão encontrado!")


#def recomendar():




