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


import pandas as pd 
#Lembrando que o caminho pode ser diferente!!
df = pd.read_excel("H:/Atividade_SI/Projeto Final/dataset_final.xlsx")

#print(df.head())

#Usar modelo - Fatoração de Matrizes - deep learning
