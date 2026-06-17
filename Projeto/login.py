import customtkinter as ctk
from tkinter import messagebox 
from banco import verificar_login

# Importar a biblioteca PIllow para arredondar os cantos
try:
    from PIL import Image, ImageTk
    PIL_disponível = True
except ImportError:
    PIL_disponível = False


#=============================
#       CORES
#=============================

FUNDO   = "#0d0d0d"
LARANJA = "#E8621A"
BRANCO  = "#FFFFFF" 
TEXTO   = "#FFFFFF"
CINZA   = "#F5F5F5"

def tela_login(janela):
    janela.title("Login")
    janela.geometry("400x560")
    janela.configure(fg_color = FUNDO)  #Cor de fundo da janela 
    janela.resizable(False,False) #Proibe do usuário aumentar a página
    
    #frame_logo = ctk.CTkFrame(janela, fg_color=FUNDO,border_width=0,bg_color = FUNDO)
    #frame_logo.pack(pady=(40, 10))

    if PIL_disponível:
        try:
            logo = ctk.CTkImage(Image.open("content/logo.png"), size=(110, 110))
            ctk.CTkLabel(janela, image=logo, text="", fg_color=FUNDO).pack(pady=(40, 10))
        except FileNotFoundError:
            ctk.CTkLabel(janela, text="📚", font=("Arial", 60), fg_color=FUNDO).pack(pady=(40, 10))
    else:
        ctk.CTkLabel(janela, text="📚", font=("Arial", 60), fg_color=FUNDO).pack(pady=(40, 10))
    #=============================
    #   ICONES
    #=============================

    icone_olho_aberto = ctk.CTkImage(Image.open("content/eye.png"), size=(22, 22))
    icone_olho_fechado = ctk.CTkImage(Image.open("content/hidden.png"), size=(22, 22))

    # ===========================================
    #       FRAME 1: LOGIN 
    # GUIAS:
    # card: Frame que envolve os campos de usuário
    # ===========================================
    card = ctk.CTkFrame(janela, fg_color = LARANJA,corner_radius=15,border_width=0) #FUndo laranja, canto arredondado
    card.pack(padx=40, fill="x",pady=(40,0))
    
    campo_layout = ctk.CTkFrame(card, fg_color=LARANJA) #Segue a mesma estrutura do card (borda)
    campo_layout.pack(padx=30,pady=(25,10),fill='x')

    #Atribuição dos parâmetros de entrada e os textos
    ctk.CTkLabel(campo_layout, text="Usuário",font=("Helvetica", 14, "bold"), text_color=BRANCO).pack(anchor='w') #w : esquerda
    entrada_usuario = ctk.CTkEntry(
        campo_layout, height=40,corner_radius=8,fg_color=CINZA, border_color=CINZA,text_color='#333', border_width=2,
        placeholder_text="Digite seu nome de usuário", placeholder_text_color='#aaa')
    entrada_usuario.pack(fill='x',pady=(5,15))
    entrada_usuario.bind("<Return>", lambda e: entrada_senha.focus()) # Vai para o proximo campo se precionar enter

    # ===========================================
    #       FRAME 2: SENHA 
    # ===========================================
    ctk.CTkLabel(campo_layout, text="Senha",font=("Helvetica", 14, "bold"), text_color=BRANCO).pack(anchor='w') #w : esquerda
    frame_senha = ctk.CTkFrame(campo_layout,fg_color=LARANJA)
    frame_senha.pack(fill='x',pady=(5,5))

    entrada_senha = ctk.CTkEntry(
        frame_senha, height=40,corner_radius=8,fg_color=CINZA, border_color=CINZA,text_color='#333', border_width=2,
        placeholder_text="Digite sua senha", placeholder_text_color='#aaa',show='*')
    entrada_senha.pack(fill='x',pady=(5,5),side='left',expand='True')
    entrada_senha.bind("<Return>", lambda e: botao_login_ativo()) # Vai para o proximo campo se precionar enter

    def visualizar_senha():
        if entrada_senha.cget("show") == "*":
            entrada_senha.configure(show="")
            botao_visualizar.configure(image=icone_olho_fechado)
        else:
            entrada_senha.configure(show="*")
            botao_visualizar.configure(image=icone_olho_aberto)
    
    botao_visualizar = ctk.CTkButton(frame_senha,text='',image=icone_olho_aberto,width=40,height=40,fg_color=CINZA, hover_color="#e0e0e0",
                        corner_radius=8,command=visualizar_senha)
    botao_visualizar.pack(side='left',padx=(5,0))
    
    # ========================= 
    #       BOTÃO LOGIN
    # ========================= 
    frame_botao = ctk.CTkFrame(card, fg_color=LARANJA) 
    frame_botao.pack(pady=(15,25))

    def botao_login_ativo():
        usuario = entrada_usuario.get()
        senha   = entrada_senha.get()

        if not usuario or not senha:
            messagebox.showwarning("Login Inválido", "Preencha usuário e senha")
            return
        if verificar_login(usuario,senha):
            messagebox.showinfo("Bem-vindo",f"{usuario}")
        else:
            messagebox.showerror("Erro","Usuário ou senha incorretos")
            entrada_usuario.delete(0,'end') #APaga os campos preenchidos
            entrada_senha.delete(0,'end')   #Apaga os campos preenchidos
            entrada_usuario.focus()
    ctk.CTkButton(
        frame_botao,
        text="Entrar",
        font=("Arial", 13, "bold"),
        fg_color=BRANCO,
        text_color=LARANJA,
        hover_color="#f0f0f0",  # cor ao passar o mouse
        corner_radius=8,
        width=200,
        height=42,
        command=botao_login_ativo,
    ).pack()
    
