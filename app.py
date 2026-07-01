import customtkinter as ctk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Sistema de Correção de Notas")
app.geometry("1200x700")
app.minsize(1000, 600)

# =========================
# CORES
# =========================

COR_FUNDO = "#07111f"
COR_MENU = "#0b1626"
COR_CARD = "#101c2e"
COR_AZUL = "#0d6efd"
COR_TEXTO = "#ffffff"
COR_TEXTO_FRACO = "#b8c1cc"

app.configure(fg_color=COR_FUNDO)

# =========================
# MENU LATERAL
# =========================

menu = ctk.CTkFrame(app, width=230, fg_color=COR_MENU, corner_radius=0)
menu.pack(side="left", fill="y")
menu.pack_propagate(False)

logo = ctk.CTkLabel(
    menu,
    text="📄✅\nSistema de\nCorreção de Notas\nVersão 1.0",
    font=("Arial", 20, "bold"),
    text_color=COR_TEXTO,
    justify="left"
)
logo.pack(padx=25, pady=(35, 25), anchor="w")


def criar_botao_menu(texto, ativo=False):
    cor = COR_AZUL if ativo else "transparent"
    return ctk.CTkButton(
        menu,
        text=texto,
        height=45,
        fg_color=cor,
        hover_color="#1d4ed8",
        anchor="w",
        corner_radius=10,
        font=("Arial", 16),
        text_color=COR_TEXTO
    )


criar_botao_menu("🏠  Início", True).pack(padx=15, pady=6, fill="x")
criar_botao_menu("🔳  Ler QR Code").pack(padx=15, pady=6, fill="x")
criar_botao_menu("📋  Provas").pack(padx=15, pady=6, fill="x")
criar_botao_menu("✅  Correção").pack(padx=15, pady=6, fill="x")
criar_botao_menu("📊  Resultados").pack(padx=15, pady=6, fill="x")
criar_botao_menu("📄  Relatórios").pack(padx=15, pady=6, fill="x")
criar_botao_menu("👥  Alunos").pack(padx=15, pady=6, fill="x")
criar_botao_menu("⚙️  Configurações").pack(padx=15, pady=6, fill="x")

usuario = ctk.CTkFrame(menu, fg_color=COR_CARD, corner_radius=15)
usuario.pack(side="bottom", padx=15, pady=20, fill="x")

ctk.CTkLabel(
    usuario,
    text="👤  Ana Cláudia",
    font=("Arial", 17, "bold"),
    text_color=COR_TEXTO
).pack(pady=(18, 2))

ctk.CTkLabel(
    usuario,
    text="Administrador",
    font=("Arial", 14),
    text_color=COR_TEXTO_FRACO
).pack()

ctk.CTkLabel(
    usuario,
    text="● Online",
    font=("Arial", 14),
    text_color="#22c55e"
).pack(pady=(8, 18))


# =========================
# CONTEÚDO PRINCIPAL
# =========================

principal = ctk.CTkFrame(app, fg_color=COR_FUNDO, corner_radius=0)
principal.pack(side="right", fill="both", expand=True)

cabecalho = ctk.CTkFrame(principal, fg_color="transparent")
cabecalho.pack(fill="x", padx=30, pady=(28, 15))

ctk.CTkLabel(
    cabecalho,
    text="Bem-vinda, Ana Cláudia! 👋",
    font=("Arial", 28, "bold"),
    text_color=COR_TEXTO
).pack(anchor="w")

ctk.CTkLabel(
    cabecalho,
    text="Gerencie suas provas e acompanhe os resultados.",
    font=("Arial", 16),
    text_color=COR_TEXTO_FRACO
).pack(anchor="w", pady=(5, 0))


# =========================
# TESTE VISUAL
# =========================

caixa = ctk.CTkFrame(principal, fg_color=COR_CARD, corner_radius=18)
caixa.pack(fill="both", expand=True, padx=30, pady=20)

ctk.CTkLabel(
    caixa,
    text="Interface moderna criada com sucesso ✅",
    font=("Arial", 26, "bold"),
    text_color=COR_TEXTO
).pack(expand=True)

print("ANTES DE ABRIR A JANELA")

app.mainloop()

print("A JANELA FECHOU")