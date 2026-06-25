import customtkinter as ctk
import pandas as pd
from tkinter import messagebox
import os

#Cores seguindo o mesmo padrão do login
FUNDO = "#1C3241"           
CARD = "#E7E1D5"            
TEXTO = "#000000"          
BOTAO_COR = "#1F6AA5"       
BOTAO_HOVER = "#144870"    
CAIXA_TEXTO_COR = "#FFFFFF" 

CAMINHO_LIVROS = "Content/dataset_final.xlsx"
CAMINHO_REVIEWS = "Content/reviews_usuarios.xlsx"


nota_selecionada = 5

# ==========================================
# FUNÇÕES DE SALVAMENTO
# ==========================================

def salvar_novo_livro(isbn, titulo, autor, ano, editora, url_capa):
    if not isbn or not titulo or not autor or not ano:
        messagebox.showwarning("Aviso", "Por favor, preencha todos os campos obrigatórios (ISBN, Título, Autor e Ano)!")
        return

    try:
        if os.path.exists(CAMINHO_LIVROS):
            df_livros = pd.read_excel(CAMINHO_LIVROS)
        else:
            df_livros = pd.DataFrame(columns=["ISBN", "Book-Title", "Book-Author", "Year-Of-Publication", "Publisher", "Image-URL-M"])

        novo_registro = {
            "ISBN": str(isbn).strip(),
            "Book-Title": titulo.strip(),
            "Book-Author": autor.strip(),
            "Year-Of-Publication": int(ano),
            "Publisher": editora.strip() if editora else "Não Informada",
            "Image-URL-M": url_capa.strip() if url_capa else "https://via.placeholder.com/120x180?text=Sem+Capa"
        }

        if str(isbn).strip() in df_livros["ISBN"].astype(str).values:
            messagebox.showerror("Erro", "Este ISBN já está cadastrado no sistema!")
            return

        df_livros = pd.concat([df_livros, pd.DataFrame([novo_registro])], ignore_index=True)
        df_livros.to_excel(CAMINHO_LIVROS, index=False)
        
        messagebox.showinfo("Sucesso", f"Livro '{titulo}' cadastrado com sucesso!")
        
    except ValueError:
        messagebox.showerror("Erro", "O campo 'Ano' deve ser um número inteiro válido.")
    except Exception as e:
        messagebox.showerror("Erro", f"Não foi possível salvar o livro: {e}")


def salvar_nova_review(usuario, titulo_livro, nota, comentario):
    if not titulo_livro:
        messagebox.showwarning("Aviso", "Por favor, preencha o nome do livro!")
        return

    try:
        if os.path.exists(CAMINHO_REVIEWS):
            df_reviews = pd.read_excel(CAMINHO_REVIEWS)
        else:
            df_reviews = pd.DataFrame(columns=["Usuário", "Livro", "Nota", "Comentário"])

        estrelas = "★" * int(nota) + "☆" * (5 - int(nota))
        item_review = f"{estrelas} {titulo_livro}"

        novo_registro = {
            "Usuário": usuario,
            "Livro": titulo_livro.strip(),
            "Nota": int(nota),
            "Comentário": comentario.strip(),
            "Texto_Formatado": item_review
        }

        df_reviews = pd.concat([df_reviews, pd.DataFrame([novo_registro])], ignore_index=True)
        df_reviews.to_excel(CAMINHO_REVIEWS, index=False)

        messagebox.showinfo("Sucesso", "Sua avaliação foi registrada com sucesso!")

    except Exception as e:
        messagebox.showerror("Erro", f"Não foi possível salvar a avaliação: {e}")

# ==========================================
# COMEÇA A INTERFACE GRÁFICA 
# ==========================================

def abrir_tela_cadastro(usuario_atual="Anônimo"):
    global nota_selecionada
    nota_selecionada = 5 

    janela_cad = ctk.CTkToplevel()
    janela_cad.title("Bookameleon - Área de Cadastro")
    janela_cad.geometry("600x720")
    janela_cad.configure(fg_color=FUNDO)
    
    # Ordem para destravar os campos de texto
    janela_cad.lift()
    janela_cad.attributes("-topmost", True)
    janela_cad.grab_set()

    # ------------------------------------------
    # BOTÃO VOLTAR -> volta pra home
    # ------------------------------------------
    frame_topo = ctk.CTkFrame(janela_cad, fg_color="transparent")
    frame_topo.pack(fill="x", padx=20, pady=(15, 0))

    btn_voltar = ctk.CTkButton(
        frame_topo,
        text="⬅ Voltar",
        font=("Arial", 12, "bold"),
        fg_color="#2A4B61",
        hover_color="#3D6A8A",
        width=150,
        height=32,
        command=janela_cad.destroy #Fecha a janela pra não travar
    )
    btn_voltar.pack(side="left")

    #Criando as Abas
    abas = ctk.CTkTabview(
        janela_cad, 
        fg_color=CARD, 
        segmented_button_selected_color=FUNDO, 
        segmented_button_unselected_color=BOTAO_COR,
        text_color="#FFFFFF"
    )
    abas.pack(fill="both", expand=True, padx=20, pady=(10, 20))
    
    aba_livro = abas.add("Cadastrar Livro")
    aba_review = abas.add("Escrever Avaliação")

    # ------------------------------------------
    # FORMULÁRIO: CADASTRAR LIVRO
    # ------------------------------------------
    ctk.CTkLabel(aba_livro, text="Adicionar Novo Livro à Base", font=("Arial", 18, "bold"), text_color=TEXTO).pack(pady=15)

    inp_isbn = ctk.CTkEntry(aba_livro, width=350, placeholder_text="ISBN*", fg_color=CAIXA_TEXTO_COR, text_color="#000000")
    inp_isbn.pack(pady=8)

    inp_titulo = ctk.CTkEntry(aba_livro, width=350, placeholder_text="Título do Livro*", fg_color=CAIXA_TEXTO_COR, text_color="#000000")
    inp_titulo.pack(pady=8)

    inp_autor = ctk.CTkEntry(aba_livro, width=350, placeholder_text="Autor*", fg_color=CAIXA_TEXTO_COR, text_color="#000000")
    inp_autor.pack(pady=8)

    inp_ano = ctk.CTkEntry(aba_livro, width=350, placeholder_text="Ano de Publicação*", fg_color=CAIXA_TEXTO_COR, text_color="#000000")
    inp_ano.pack(pady=8)

    inp_editora = ctk.CTkEntry(aba_livro, width=350, placeholder_text="Editora", fg_color=CAIXA_TEXTO_COR, text_color="#000000")
    inp_editora.pack(pady=8)

    inp_url = ctk.CTkEntry(aba_livro, width=350, placeholder_text="URL da Imagem da Capa", fg_color=CAIXA_TEXTO_COR, text_color="#000000")
    inp_url.pack(pady=8)

    def acao_cadastrar_livro():
        salvar_novo_livro(
            inp_isbn.get(), inp_titulo.get(), inp_autor.get(), 
            inp_ano.get(), inp_editora.get(), inp_url.get()
        )
        inp_isbn.delete(0, 'end'); inp_titulo.delete(0, 'end'); inp_autor.delete(0, 'end')
        inp_ano.delete(0, 'end'); inp_editora.delete(0, 'end'); inp_url.delete(0, 'end')

    btn_salvar_livro = ctk.CTkButton(
        aba_livro, 
        text="Salvar Livro", 
        fg_color=BOTAO_COR, 
        hover_color=BOTAO_HOVER, 
        font=("Arial", 14, "bold"),
        width=180,
        height=38,
        command=acao_cadastrar_livro
    )
    btn_salvar_livro.pack(pady=20)

    # ------------------------------------------
    # FORMULÁRIO: CADASTRAR REVIEW
    # ------------------------------------------
    ctk.CTkLabel(aba_review, text="Deixe sua Opinião", font=("Arial", 18, "bold"), text_color=TEXTO).pack(pady=15)

    inp_livro_review = ctk.CTkEntry(aba_review, width=350, placeholder_text="Nome do Livro", fg_color="#FFFFFF", text_color="#000000")
    inp_livro_review.pack(pady=8)

    # Nota em formato de Combobox (1 a 5 estrelas)
    ctk.CTkLabel(aba_review, text="Sua Nota (1 a 5 estrelas):", text_color=TEXTO).pack(pady=(5,0))
    combo_nota = ctk.CTkComboBox(aba_review, values=["5", "4", "3", "2", "1"], width=100, fg_color="#FFFFFF", text_color="#000000")
    combo_nota.pack(pady=5)

    ctk.CTkLabel(aba_review, text="Comentário:", text_color=TEXTO).pack(pady=(5,0))
    inp_comentario = ctk.CTkTextbox(aba_review, width=350, height=120, fg_color="#FFFFFF", text_color="#000000")
    inp_comentario.pack(pady=5)

    def acao_cadastrar_review():
        salvar_nova_review(
            usuario_atual,
            inp_livro_review.get(),
            combo_nota.get(),
            inp_comentario.get("1.0", "end-1c")
        )
        inp_livro_review.delete(0, 'end')
        inp_comentario.delete("1.0", "end")

    btn_salvar_review = ctk.CTkButton(aba_review, text="Publicar Avaliação", fg_color=FUNDO, hover_color=BOTAO_COR, command=acao_cadastrar_review)
    btn_salvar_review.pack(pady=20)

    return janela_cad