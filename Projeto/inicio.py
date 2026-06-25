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
    livros = pd.read_excel("Content/dataset_final.xlsx", engine="openpyxl", dtype={"ISBN": str})

    if "ISBN" in livros.columns:
        livros["ISBN"] = livros["ISBN"].astype(str).str.split('.').str[0].str.strip()
    else:
        print("Erro: Coluna 'ISBN' não encontrada no arquivo.")
        livros = None
except FileNotFoundError:
    print("Erro: Arquivo 'Content/dataset_final.xlsx' não encontrado.")
    livros = None
except Exception as e:
    print(f"Ocorreu um erro ao carregar o arquivo: {e}")
    livros = None

# ==========================================
# TELA INICIAL
# ==========================================

def tela_inicio(janela, usuario_logado, usuario, sugestoes):

    janela.title("Tela inicial")
    janela.geometry("600x750")
    janela.configure(fg_color=FUNDO)

    # ==========================================
    # FUNÇÕES AUXILIARES
    # ==========================================

    def ir_para_cadastro():
        import cadastro_livros
        cadastro_livros.abrir_tela_cadastro(usuario)

    def image_url(url, tamanho=(24, 24)):
        if not url or not isinstance(url, str) or url.strip() == "" or url == "nan":
            return None
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
                'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
                'Referer': 'https://www.google.com/',
                'Connection': 'keep-alive'
            }
            getter = requests.get(url.strip(), headers=headers, timeout=5)
            getter.raise_for_status()
            img_data = BytesIO(getter.content)
            img_open = Image.open(img_data)
            return ctk.CTkImage(img_open, size=tamanho)
        except Exception as e:
            print(f"Erro ao carregar imagem da URL ({url}):", e)
            return None

    def carregar_capa_thread(url, widget, titulo):
        capa = image_url(url, tamanho=(90, 150))
        if capa:
            widget.after(0, lambda: widget.configure(image=capa, text=""))
            widget.image = capa
        else:
            titulo_formatado = titulo if isinstance(titulo, str) else "Titulo Desconhecido"
            widget.after(0, lambda: widget.configure(text=titulo_formatado[:15] + "..."))

    # ==========================================
    # CONTAINER COM SCROLL VERTICAL
    # ==========================================

    container_principal = ctk.CTkScrollableFrame(
        janela,
        orientation="vertical",
        fg_color=FUNDO
    )
    container_principal.pack(fill="both", expand=True)

    # ==========================================
    # TOPO
    # ==========================================

    topo = ctk.CTkFrame(container_principal, fg_color="transparent")
    topo.pack(fill="x", padx=20, pady=15, anchor="w")

    try:
        imagem_logo_pil = Image.open("Content/logo.png")
        logo_image = ctk.CTkImage(
            light_image=imagem_logo_pil,
            dark_image=imagem_logo_pil,
            size=(40, 40)
        )
        logo_container = ctk.CTkFrame(topo, fg_color="transparent")
        logo_container.pack(side="left")
        lbl_logo = ctk.CTkLabel(logo_container, image=logo_image, text="")
        lbl_logo.pack(side="left", padx=(0, 10))
    except Exception as e:
        print(f"Erro ao carregar a logo: {e}")
        ctk.CTkLabel(topo, text="", font=("Arial", 28, "bold")).pack(side="left")

    busca = ctk.CTkEntry(topo, width=350, height=40, placeholder_text="Buscar livro...")
    busca.pack(side="left", padx=50)

    ctk.CTkLabel(topo, text=f"Olá, {usuario}!", font=("Arial", 18, "bold")).pack(side="right")

    # ==========================================
    # RECOMENDADOS
    # ==========================================

    ctk.CTkLabel(
        container_principal,
        text="Recomendados para você",
        font=("Arial", 22, "bold")
    ).pack(anchor="w", padx=30, pady=(15, 5))

    frame_livros_scrollable = ctk.CTkScrollableFrame(
        container_principal,
        orientation="horizontal",
        height=280,
        fg_color="transparent"
    )
    frame_livros_scrollable.pack(fill="x", padx=20, pady=5)

    if sugestoes:
        for i, (isbn, nota, url_da_capa, titulo_livro) in enumerate(sugestoes):
            livro_df = livros[livros["ISBN"] == str(isbn)]

            if not livro_df.empty:
                autor = livro_df.iloc[0]["Book-Author"]
                ano = livro_df.iloc[0]["Year-Of-Publication"]
            else:
                autor = "Autor não consta no banco de Dados"
                ano = "Não informado"

            card = ctk.CTkFrame(frame_livros_scrollable, width=180, height=250, fg_color=CARD, corner_radius=12)
            card.pack(side="left", padx=8, pady=5)
            card.pack_propagate(False)

            label_imagem = ctk.CTkLabel(card, text="Carregando...", text_color="#1C3241", font=("Arial", 10, "bold"))
            label_imagem.pack(pady=(10, 5), expand=True)

            if url_da_capa and str(url_da_capa) != "nan":
                threading.Thread(target=carregar_capa_thread, args=(url_da_capa, label_imagem, titulo_livro), daemon=True).start()
            else:
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
    # AVALIAÇÕES RECENTES
    # ==========================================

    avaliacoes = ctk.CTkFrame(container_principal, fg_color=CARD, corner_radius=12)
    avaliacoes.pack(fill="x", padx=30, pady=10)

    ctk.CTkLabel(
        avaliacoes,
        text="Avaliações Recentes",
        font=("Arial", 22, "bold"),
        text_color=TEXTO
    ).pack(anchor="w", padx=15, pady=15)

    exemplos = [
        "★★★★★ O Hobbit",
        "★★★★☆ Harry Potter",
        "★★★★★ Senhor dos Anéis",
        "★★★★☆ Código Da Vinci"
    ]

    for item in exemplos:
        ctk.CTkLabel(avaliacoes, text=item, text_color=TEXTO, font=("Arial", 14)).pack(anchor="w", padx=20, pady=2)

    # ==========================================
    # CADASTRO DE LIVROS
    # ==========================================

    painel_usuario = ctk.CTkFrame(container_principal, fg_color="transparent")
    painel_usuario.pack(fill="x", padx=30, pady=(20, 30))

    ctk.CTkLabel(painel_usuario, text="Reviews", font=("Arial", 22, "bold")).pack(side="left")

    ctk.CTkButton(
        painel_usuario,
        text="➕ Cadastrar Livros ou Avaliações",
        font=("Arial", 14, "bold"),
        width=250,
        height=40,
        fg_color="#2A4B61",
        hover_color="#3D6A8A",
        command=ir_para_cadastro
    ).pack(side="right")
