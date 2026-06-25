import customtkinter as ctk
import pandas as pd
import requests
import threading

from PIL import Image
from io import BytesIO

# ==========================================
# CONFIGURAÇÕES
# ==========================================

FUNDO = "#1C3241"
CARD = "#E7E1D5"
TEXTO = "#000000"

# ==========================================
# CARREGA BASE DE LIVROS
# ==========================================

try:
    livros = pd.read_excel("Content/dataset_final.xlsx",engine="openpyxl", dtype={"ISBN": str}) # Usar read_excel para .xlsx
    # livros.columns = livros.columns.str.strip() # Descomentar se houver espaços nos nomes das colunas

    if "ISBN" in livros.columns:
        livros["ISBN"] = livros["ISBN"].astype(str).str.split('.').str[0].str.strip() #Limpa qualquer tipo de erro que pode ter na extração do ISBN
    else:
        print("Erro: Coluna 'ISBN' não encontrada no arquivo.")
        livros = None # Ou lidar com o erro de outra forma
except FileNotFoundError:
    print("Erro: Arquivo 'Content/dataset_final.xlsx' não encontrado.")
    livros = None # Ou lidar com o erro de outra forma
except Exception as e:
    print(f"Ocorreu um erro ao carregar o arquivo: {e}")
    livros = None

# ==========================================
# TELA INICIAL
# ==========================================

def tela_inicio(janela, usuario_logado, usuario, sugestoes):

    janela.title("Tela inicial")
    janela.geometry("600X650")
    janela.configure(fg_color=FUNDO)

    # ==========================================
    #       FUNÇÕES AUXILIARES  
    #==========================================
    def image_url(url, tamanho=(24, 24)):
        # Ignora URL vazio
        if not url or not isinstance(url, str) or url.strip() == "" or url == "nan":
            return None
        try:
            # Amazon bloqueia acessos que são considerados como "bot", portanto, headers seria um meio de solução para conseguir acessar
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
                'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
                'Referer': 'https://www.google.com/',
                'Connection': 'keep-alive'
            }
            #Requisição de URL usando os cabeçalhos
            getter = requests.get(url.strip(), headers=headers, timeout=5)
            getter.raise_for_status() 
            
            img_data = BytesIO(getter.content)  #MetaDados da imagem (converte bytes em um arquivo de imagem na memória)
            img_open = Image.open(img_data)
            return ctk.CTkImage(img_open, size=tamanho)
        except Exception as e:
            print(f"Erro ao carregar imagem da URL ({url}):", e)
            return None
        
    # Como o dataset é muito denso, thread ajuda a fazer esse processo de forma simultanea, reduzindo um pouco do tempo de retorno
    # -> Função que carrega as capas com base no URL
    def carregar_capa_thread(url, widget, titulo):
        capa = image_url(url, tamanho=(90, 150)) #Faz a requisição e pega a imagem
        if capa:  #Se capa não for vazia, mostra a imagem assim que conseguir (atualiza aos poucos)
            widget.after(0, lambda: widget.configure(image=capa, text=""))
            widget.image = capa # Salva a imagem para não ser perdida
        else: 
            # Verifica se o titulo é um texto válido
            titulo_formatado = titulo if isinstance(titulo, str) else "Titulo Desconhecido" 
            widget.after(0, lambda: widget.configure(text=titulo_formatado[:15]+"...")) # Atualiza a tela, mostra o TItulo ao invés da capa

    # ==========================================
    # TOPO
    # ==========================================


    topo = ctk.CTkFrame(
        janela,
        fg_color="transparent"
    )
    topo.pack(fill="x", padx=20, pady=15, anchor="w")

    try:
        # Carrega a imagem da logo usando PIL
        imagem_logo_pil = Image.open("Content/logo.png")
        
        # Converte para CTkImage (ajuste o size se achar que ficou grande ou pequena)
        logo_image = ctk.CTkImage(
            light_image=imagem_logo_pil,
            dark_image=imagem_logo_pil,
            size=(40, 40)  # Altura combinando com a barra de busca
        )
        
        # Cria o frame que vai juntar a Logo + Texto do título do lado esquerdo
        logo_container = ctk.CTkFrame(topo, fg_color="transparent")
        logo_container.pack(side="left")
        
        # Label da imagem
        lbl_logo = ctk.CTkLabel(logo_container, image=logo_image, text="")
        lbl_logo.pack(side="left", padx=(0, 10))
        
        
    except Exception as e:
        # Caso a logo não seja encontrada, exibe o texto padrão para não quebrar o app
        print(f"Erro ao carregar a logo: {e}")
        ctk.CTkLabel(
            topo,
            text="",
            font=("Arial", 28, "bold")
        ).pack(side="left")


    busca = ctk.CTkEntry(
        topo,
        width=350,
        height=40,
        placeholder_text="Buscar livro..."
    )
    busca.pack(side="left", padx=50)
    
    ctk.CTkLabel(
        topo,
        text=f"Olá, {usuario}!",
        font=("Arial", 18, "bold")
    ).pack(side="right")

    # ==========================================
    # RECOMENDADOS
    # ==========================================
    ctk.CTkLabel(
        janela,
        text="Recomendados para você",
        font=("Arial", 22, "bold")
    ).pack(anchor="w", padx=30, pady=(15, 5))
    frame_livros_scrollable = ctk.CTkScrollableFrame( 
        janela,
        orientation="horizontal",
        height=280, 
        fg_color="transparent"
    )
    frame_livros_scrollable.pack(
        fill="x",
        padx=20,
        pady=5
    )
    if sugestoes:
        # Percorre a lista de sugestões gerada pelo algoritmo
        for i, (isbn, nota, url_da_capa, titulo_livro) in enumerate(sugestoes):
            #Procura detalhes dos livros (Ano, author e url)
            livro_df = livros[livros["ISBN"] == str(isbn)] 
            
            if not livro_df.empty: # Se o livro tiver sido encontrado
                autor = livro_df.iloc[0]["Book-Author"] 
                ano = livro_df.iloc[0]["Year-Of-Publication"] 
            else:
                autor = "Autor não consta no banco de Dados"
                ano = "Não informado"

            #Card dos livros
            card = ctk.CTkFrame(frame_livros_scrollable, width=180, height=250, fg_color=CARD, corner_radius=12)
            card.pack(side="left", padx=8, pady=5)
            card.pack_propagate(False)
            #Textos embaixo da imagem (AUtor, ano)
            label_imagem = ctk.CTkLabel(card, text="Carregando...", text_color="#1C3241", font=("Arial", 10, "bold"))
            label_imagem.pack(pady=(10, 5), expand=True)

            # Dispara a Thread para baixar a imagem
            if url_da_capa and str(url_da_capa) != "nan":
                threading.Thread(target=carregar_capa_thread, args=(url_da_capa, label_imagem, titulo_livro), daemon=True).start()
            else: #Imagem Default
                label_imagem.configure(text="📚", font=("Arial", 40))

            titulo_formatado = str(titulo_livro)
            if len(titulo_formatado) > 25:
                titulo_formatado = titulo_formatado[:22] + "..."

            ctk.CTkLabel(card, text=titulo_formatado, text_color=TEXTO, font=("Arial", 11, "bold")).pack(padx=5, pady=0)
            ctk.CTkLabel(card, text=autor, text_color=TEXTO, font=("Arial", 10)).pack(pady=0)
            nota_prevista = f"Nota: {nota:.2f}" if isinstance(nota, (int, float)) else f"{nota}"
            ctk.CTkLabel(card, text=nota_prevista, text_color="#1C3241", font=("Arial", 9, "bold")).pack(pady=0)
            ctk.CTkLabel(card, text=f"Ano: {ano}", text_color=TEXTO, font=("Arial", 9)).pack(pady=(0, 5))
    
    else:
        ctk.CTkLabel(frame_livros_scrollable, text="Nenhuma recomendação disponível para este perfil.").pack(pady=40)
    # ==========================================
    # CATEGORIAS
    # ==========================================

    categorias = ctk.CTkFrame(
        janela,
        fg_color="transparent"
    )

    categorias.pack(
        fill="x",
        padx=30,
        pady=20
    )

    ctk.CTkLabel(
        categorias,
        text="Categorias",
        font=("Arial", 22, "bold")
    ).pack(anchor="w")

    frame_cat = ctk.CTkFrame(
        categorias,
        fg_color="transparent"
    )

    frame_cat.pack(
        anchor="w",
        pady=10
    )

    lista = [
        "Romance",
        "Fantasia",
        "Terror",
        "Ficção",
        "Drama",
        "Mistério"
    ]

    for categoria in lista:

        ctk.CTkButton(
            frame_cat,
            text=categoria,
            width=120,
            height=35
        ).pack(side="left", padx=5)

    # ==========================================
    # AVALIAÇÕES RECENTES
    # ==========================================

    avaliacoes = ctk.CTkFrame(
        janela,
        fg_color=CARD,
        corner_radius=12
    )

    avaliacoes.pack(
        fill="both",
        expand=True,
        padx=30,
        pady=10
    )

    ctk.CTkLabel(
        avaliacoes,
        text="Avaliações Recentes",
        font=("Arial", 22, "bold"),
        text_color=TEXTO
    ).pack(
        anchor="w",
        padx=15,
        pady=15
    )

    exemplos = [
        "★★★★★ O Hobbit",
        "★★★★☆ Harry Potter",
        "★★★★★ Senhor dos Anéis",
        "★★★★☆ Código Da Vinci"
    ]

    for item in exemplos:

        ctk.CTkLabel(
            avaliacoes,
            text=item,
            text_color=TEXTO,
            font=("Arial", 14)
        ).pack(
            anchor="w",
            padx=20,
            pady=2
        )
