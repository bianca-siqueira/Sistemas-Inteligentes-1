import customtkinter as ctk
from tkinter import messagebox
from banco import cadastrar_usuario

try:
    from PIL import Image, ImageTk
    PIL_disponível = True
except ImportError:
    PIL_disponível = False

#=============================
#       CORES 
#=============================
FUNDO   = "#1C3241"
LARANJA = "#E7E1D5"
BRANCO  = "#000000"
TEXTO   = "#000000"
CINZA   = "#F5F5F5"

def tela_cadastro(janela, ao_cadastrar=None):

    janela.title("Cadastro")
    janela.geometry("400x660")
    janela.configure(fg_color=FUNDO)
    janela.resizable(False, False)

    #=============================
    #   ICONES
    #=============================

    # Tenta carregar a logo do app, se não encontrar, usa emoji
    if PIL_disponível:
        try:
            logo = ctk.CTkImage(Image.open("content/logo.png"), size=(180, 153))
            ctk.CTkLabel(janela, image=logo, text="", fg_color=FUNDO).pack(pady=(10, 10))
        except FileNotFoundError:
            ctk.CTkLabel(janela, text="📚", font=("Arial", 60), fg_color=FUNDO).pack(pady=(40, 10))
    else:
        ctk.CTkLabel(janela, text="📚", font=("Arial", 60), fg_color=FUNDO).pack(pady=(40, 10))
    
    icone_olho_aberto = ctk.CTkImage(Image.open("content/eye.png"), size=(22, 22))
    icone_olho_fechado = ctk.CTkImage(Image.open("content/hidden.png"), size=(22, 22))


    # ===========================================
    #       FRAME 1: CARD COM CADASTRO 
    # GUIAS:
    # card: Frame que envolve os campos de usuário
    # Campo_layout: frame interno que organiza os campos 
    # ===========================================

    card = ctk.CTkFrame(janela, fg_color=LARANJA, corner_radius=15, border_width=0)
    card.pack(padx=40, fill="x", pady=(20, 0))

    campo_layout = ctk.CTkFrame(card, fg_color=LARANJA)
    campo_layout.pack(padx=30, pady=(25, 10), fill="x")

    # CAMPO 1: USUARIO
    ctk.CTkLabel(campo_layout, text="Usuário",
                 font=("Helvetica", 14, "bold"), text_color=BRANCO).pack(anchor="w")

    entrada_usuario = ctk.CTkEntry(
        campo_layout, height=40, corner_radius=8,
        fg_color=CINZA, border_color=CINZA, text_color="#333",
        border_width=2, placeholder_text="Escolha um nome de usuário",
        placeholder_text_color="#aaa"
    )
    entrada_usuario.pack(fill="x", pady=(5, 15))
    entrada_usuario.bind("<Return>", lambda e: entrada_senha.focus()) # Enter avança para o proximo campo

     # CAMPO 2: SENHA 
    ctk.CTkLabel(campo_layout, text="Senha",
                 font=("Helvetica", 14, "bold"), text_color=BRANCO).pack(anchor="w")

    # AGrupa o campo de texto com o botão de olho
    frame_senha = ctk.CTkFrame(campo_layout, fg_color=LARANJA)
    frame_senha.pack(fill="x", pady=(5, 5))

    entrada_senha = ctk.CTkEntry(
        frame_senha, height=40, corner_radius=8,
        fg_color=CINZA, border_color=CINZA, text_color="#333",
        border_width=2, placeholder_text="Crie uma senha",
        placeholder_text_color="#aaa", show="*"
    )
    entrada_senha.pack(fill="x", pady=(5, 5), side="left", expand=True)
    entrada_senha.bind("<Return>", lambda e: entrada_confirmar.focus())

    # Muda o modo de visualização de senha (oculto ou normal)
    def visualizar_senha():
        if entrada_senha.cget("show") == "*":
            entrada_senha.configure(show="")
            botao_vis_senha.configure(image=icone_olho_fechado)
        else:
            entrada_senha.configure(show="*")
            botao_vis_senha.configure(image=icone_olho_aberto)

    botao_vis_senha = ctk.CTkButton(
        frame_senha, text="",
        image=icone_olho_aberto,
        width=40, height=40, fg_color=CINZA, hover_color="#e0e0e0",
        corner_radius=8, command=visualizar_senha
    )
    botao_vis_senha.pack(side="left", padx=(5, 0))

    # CAMPO 3: CONFIRMAR SENHA
    ctk.CTkLabel(campo_layout, text="Confirmar Senha",
                 font=("Helvetica", 14, "bold"), text_color=BRANCO).pack(anchor="w", pady=(10, 0))

    frame_confirmar = ctk.CTkFrame(campo_layout, fg_color=LARANJA)
    frame_confirmar.pack(fill="x", pady=(5, 5))

    entrada_confirmar = ctk.CTkEntry(
        frame_confirmar, height=40, corner_radius=8,
        fg_color=CINZA, border_color=CINZA, text_color="#333",
        border_width=2, placeholder_text="Repita a senha",
        placeholder_text_color="#aaa", show="*"
    )
    entrada_confirmar.pack(fill="x", pady=(5, 5), side="left", expand=True)
    entrada_confirmar.bind("<Return>", lambda e: botao_cadastrar_ativo())

    # Muda o modo de visualização de senha (oculto ou normal)
    def visualizar_confirmar():
        if entrada_confirmar.cget("show") == "*":
            entrada_confirmar.configure(show="")
            botao_vis_confirmar.configure(image=icone_olho_fechado)
        else:
            entrada_confirmar.configure(show="*")
            botao_vis_confirmar.configure(image=icone_olho_aberto)

    botao_vis_confirmar = ctk.CTkButton(
        frame_confirmar, text="",
        image=icone_olho_aberto,
        width=40, height=40, fg_color=CINZA, hover_color="#e0e0e0",
        corner_radius=8, command=visualizar_confirmar
    )
    botao_vis_confirmar.pack(side="left", padx=(5, 0))

    # ===========================================
    #       BOTAO CADASTRO
    # ===========================================

    frame_botao = ctk.CTkFrame(card, fg_color=LARANJA)
    frame_botao.pack(pady=(15, 25))

    def botao_cadastrar_ativo():
        usuario   = entrada_usuario.get().strip()
        senha     = entrada_senha.get()
        confirmar = entrada_confirmar.get()

        if not usuario or not senha or not confirmar:
            messagebox.showwarning("Campos vazios", "Preencha todos os campos.")
            return

        if senha != confirmar:
            messagebox.showerror("Erro", "As senhas não coincidem.")
            entrada_senha.delete(0, "end")
            entrada_confirmar.delete(0, "end")
            entrada_senha.focus()
            return

        if len(senha) < 6:
            messagebox.showwarning("Senha fraca", "A senha deve ter pelo menos 6 caracteres.")
            entrada_senha.delete(0, "end")
            entrada_confirmar.delete(0, "end")
            return

        sucesso = cadastrar_usuario(usuario, senha)

        if sucesso:
            messagebox.showinfo("Cadastro realizado", f"Bem-vindo, {usuario}!")
            ir_para_inicio()   # Vai para a tela de inicio
        else:
            messagebox.showerror("Erro", f"O usuário '{usuario}' já existe. Escolha outro nome.")
            entrada_usuario.delete(0, "end")
            entrada_usuario.focus()

    ctk.CTkButton(
        frame_botao,
        text="Cadastrar",
        font=("Arial", 13, "bold"),
        fg_color=BRANCO,
        text_color=LARANJA,
        hover_color="#242424",
        corner_radius=8,
        width=200,
        height=42,
        command=botao_cadastrar_ativo,
    ).pack()

    # VAI PARA A PÁGINA INICIAL
    def ir_para_inicio():
        janela.destroy()
        #nova_janela = ctk.CTk()
        #tela_inicial(nova_janela)
        #nova_janela.mainloop()
    def ir_para_login():
        from login import tela_login
        janela.destroy()
        nova_janela = ctk.CTk()
        tela_login(nova_janela)
        nova_janela.mainloop()

    ctk.CTkButton(
        frame_botao,
        text="Já possui conta? Entrar",
        font=("Arial", 11),
        fg_color="transparent",
        text_color="#6B8FA3",
        hover_color=LARANJA,
        hover=True,
        corner_radius=8,
        width=200,
        height=30,
        command=ir_para_login,
    ).pack(pady=(8, 0))
>>>>>>> 2f13fc9 (Implementação Tela de Cadastro)
