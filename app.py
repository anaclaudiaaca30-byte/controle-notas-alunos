import customtkinter as ctk
from tkinter import messagebox
from tkinter import ttk
from tkinter import filedialog
from datetime import datetime
import sqlite3
from PIL import Image, ImageTk
import cv2
import os
import easyocr
import traceback
import numpy as np

# =========================
# CONFIGURAÇÃO DA JANELA
# =========================

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Sistema de Correção de Notas")
app.geometry("1200x700")

# =========================
# CORES
# =========================

COR_FUNDO = "#06081E"
COR_MENU = "#101A40"

COR_CARD1 = "#1877F2"      # Azul
COR_CARD2 = "#22C55E"      # Verde
COR_CARD3 = "#F97316"      # Laranja
COR_CARD4 = "#EC4899"      # Rosa
COR_CARD5 = "#7C3AED"      # Roxo

COR_TEXTO = "#FFFFFF"
COR_SUBTITULO = "#D1D5DB"
COR_TEXTO_FRACO = "#9CA3AF"
COR_CARD = "#152238"
COR_AZUL = COR_CARD1
COR_HOVER = "#8B5CF6"
COR_BOTAO = "#1E293B"

app.configure(fg_color=COR_FUNDO)

# =========================
# BANCO DE DADOS
# =========================

conexao = sqlite3.connect("alunos.db")
cursor = conexao.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS medias_alunos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT,
    nota1 REAL,
    nota2 REAL,
    nota3 REAL,
    media REAL,
    faltas INTEGER,
    limite_faltas INTEGER,
    situacao TEXT,
    data TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS atividades (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    aluno TEXT,
    disciplina TEXT,
    tipo_atividade TEXT,
    caminho_imagem TEXT,
    resultado TEXT,
    nota REAL,
    status TEXT,
    data_captura TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS provas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome_prova TEXT,
    disciplina TEXT,
    tema TEXT,
    gabarito TEXT,
    sugestoes TEXT,
    data_criacao TEXT
)
""")

conexao.commit()

# =========================
# FUNÇÕES
# =========================

def limpar_principal():
    for widget in principal.winfo_children():
        widget.destroy()


def criar_titulo(titulo, subtitulo):
    label_titulo = ctk.CTkLabel(
        principal,
        text=titulo,
        font=("Segoe UI", 32, "bold"),
        text_color=COR_TEXTO
    )
    label_titulo.pack(anchor="w", padx=30, pady=(25, 5))

    label_subtitulo = ctk.CTkLabel(
        principal,
        text=subtitulo,
        font=("Arial", 16),
        text_color=COR_TEXTO_FRACO
    )
    label_subtitulo.pack(anchor="w", padx=30, pady=(0, 20))


def tela_inicio():
    limpar_principal()
    criar_titulo("Bem-vinda, Ana Cláudia! 👋", "Gerencie suas provas e acompanhe os resultados.")

    card = ctk.CTkFrame(principal, fg_color=COR_CARD, corner_radius=18)
    card.pack(fill="both", expand=True, padx=30, pady=20)

    texto = ctk.CTkLabel(
        card,
        text="Sistema de Correção de Notas\nVersão 1.0",
        font=("Arial", 28, "bold"),
        text_color=COR_TEXTO
    )
    texto.pack(expand=True)


def tela_simples(nome):
    limpar_principal()
    criar_titulo(nome, "Tela em desenvolvimento.")

    card = ctk.CTkFrame(principal, fg_color=COR_CARD, corner_radius=18)
    card.pack(fill="both", expand=True, padx=30, pady=20)

    texto = ctk.CTkLabel(
        card,
        text=f"{nome}\n\nEssa parte será criada nas próximas etapas.",
        font=("Arial", 22, "bold"),
        text_color=COR_TEXTO
    )
    texto.pack(expand=True)


def gerar_sugestoes_provas(disciplina, tema):
    disc = disciplina.strip().lower()
    tema = tema.strip().lower()

    if "matem" in disc:
        assuntos = ["Frações", "Equações de 1º grau", "Porcentagem", "Geometria plana"]
        if "fraç" in tema:
            sugestoes = [
                "Resolva 3 questões sobre comparação de frações.",
                "Transforme frações impróprias em números mistos.",
                "Calcule o valor de uma fração de um número."
            ]
        elif "equação" in tema:
            sugestoes = [
                "Resolva uma equação do 1º grau com uma incógnita.",
                "Monte uma equação a partir de um problema cotidiano.",
                "Verifique se um valor satisfaz a equação dada."
            ]
        else:
            sugestoes = [
                "Resolva problemas envolvendo porcentagem.",
                "Calcule a área de figuras planas.",
                "Simplifique expressões numéricas."
            ]
    elif "port" in disc or "língua" in disc:
        assuntos = ["Interpretação de texto", "Classes gramaticais", "Ortografia", "Redação"]
        sugestoes = [
            "Identifique o sujeito e o predicado de uma frase.",
            "Explique o sentido de uma palavra em contexto.",
            "Faça uma pequena redação sobre um tema escolar."
        ]
    elif "hist" in disc:
        assuntos = ["Brasil Colonial", "Era Vargas", "Segunda Guerra Mundial", "Direitos Humanos"]
        sugestoes = [
            "Explique as causas de um evento histórico importante.",
            "Compare dois períodos históricos.",
            "Liste mudanças sociais de um tema estudado."
        ]
    else:
        assuntos = ["Planejamento", "Avaliação", "Contexto", "Objetivo"]
        sugestoes = [
            "Descreva o tema central da prova.",
            "Elabore uma questão de múltipla escolha com 4 alternativas.",
            "Crie uma questão dissertativa com pedido claro."
        ]

    texto = "Sugestões de questões:\n"
    for item in sugestoes:
        texto += f"• {item}\n"
    texto += "\nAssuntos relacionados:\n"
    for item in assuntos:
        texto += f"• {item}\n"

    return texto


def tela_provas():
    limpar_principal()
    criar_titulo("📝 Provas", "Cadastre provas e receba sugestões de questões para usar como modelo.")

    card = ctk.CTkFrame(principal, fg_color=COR_CARD, corner_radius=18)
    card.pack(fill="both", expand=True, padx=30, pady=20)

    form = ctk.CTkFrame(card, fg_color="transparent")
    form.pack(fill="x", padx=30, pady=(0, 10))

    entrada_nome_prova = ctk.CTkEntry(form, placeholder_text="Nome da prova", width=300, height=40)
    entrada_nome_prova.grid(row=0, column=0, padx=10, pady=10)
    entrada_disciplina = ctk.CTkEntry(form, placeholder_text="Disciplina", width=220, height=40)
    entrada_disciplina.grid(row=0, column=1, padx=10, pady=10)
    entrada_tema = ctk.CTkEntry(form, placeholder_text="Tema / assunto", width=220, height=40)
    entrada_tema.grid(row=0, column=2, padx=10, pady=10)
    entrada_gabarito = ctk.CTkEntry(form, placeholder_text="Gabarito (ex: A,B,C,D)", width=760, height=40)
    entrada_gabarito.grid(row=1, column=0, columnspan=3, padx=10, pady=10)

    sugestoes_label = ctk.CTkLabel(
        card,
        text="As sugestões aparecerão aqui quando você clicar em Gerar sugestões.",
        width=880,
        height=220,
        fg_color="#151f30",
        corner_radius=15,
        font=("Arial", 14),
        text_color=COR_TEXTO,
        justify="left",
        wraplength=860
    )
    sugestoes_label.pack(fill="x", padx=30, pady=(0, 20))

    def gerar_sugestoes():
        disciplina = entrada_disciplina.get().strip()
        tema = entrada_tema.get().strip()
        texto = gerar_sugestoes_provas(disciplina, tema)
        sugestoes_label.configure(text=texto)

    def salvar_prova():
        nome_prova = entrada_nome_prova.get().strip() or "Prova sem nome"
        disciplina = entrada_disciplina.get().strip() or "Sem disciplina"
        tema = entrada_tema.get().strip() or "Sem tema"
        gabarito = entrada_gabarito.get().strip() or ""
        sugestoes = sugestoes_label.cget("text")
        data_criacao = datetime.now().strftime("%d/%m/%Y %H:%M")

        cursor.execute("""
            INSERT INTO provas (
                nome_prova,
                disciplina,
                tema,
                gabarito,
                sugestoes,
                data_criacao
            ) VALUES (?, ?, ?, ?, ?, ?)
        """, (
            nome_prova,
            disciplina,
            tema,
            gabarito,
            sugestoes,
            data_criacao
        ))
        conexao.commit()

        messagebox.showinfo("Prova salva", "Prova registrada no banco de dados.")

    botoes = ctk.CTkFrame(card, fg_color="transparent")
    botoes.pack(fill="x", padx=30, pady=(0, 10))

    ctk.CTkButton(botoes, text="💡 Gerar sugestões", width=220, command=gerar_sugestoes).pack(side="left", padx=10)
    ctk.CTkButton(botoes, text="💾 Salvar prova", width=220, fg_color=COR_AZUL, command=salvar_prova).pack(side="left", padx=10)

def corrigir_atividade_com_ia(caminho_imagem):
    try:
        import base64
        import os
        from openai import OpenAI

        # Verifica se a imagem existe
        if not os.path.exists(caminho_imagem):
            return "Erro: imagem não encontrada."

        # Busca a chave da OpenAI nas variáveis do Windows
        chave = os.getenv("OPENAI_API_KEY")

        if not chave:
            return (
                "A chave OPENAI_API_KEY não foi encontrada.\n"
                "Configure a chave da OpenAI antes de usar a correção com IA."
            )

        cliente = OpenAI(api_key=chave)

        # Converte a imagem para Base64
        with open(caminho_imagem, "rb") as arquivo:
            imagem_base64 = base64.b64encode(
                arquivo.read()
            ).decode("utf-8")

        # Envia a atividade para análise
        resposta = cliente.responses.create(
            model="gpt-5.6-luna",
            input=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "input_text",
                            "text": """
Analise cuidadosamente esta atividade escolar.

Sua tarefa é:

1. Ler todo o texto visível da atividade.
2. Identificar as questões.
3. Identificar as respostas dadas pelo aluno.
4. Não inventar palavras que não estejam legíveis.
5. Quando alguma parte não puder ser lida,
   informe [ilegível].
6. Organizar o resultado por questão.

Ainda não atribua nota.

Apresente no formato:

QUESTÃO 1:
Enunciado:
Resposta do aluno:

QUESTÃO 2:
Enunciado:
Resposta do aluno:

Continue dessa maneira para todas as questões
que conseguir identificar.
"""
                        },
                        {
                            "type": "input_image",
                            "image_url":
                                f"data:image/jpeg;base64,{imagem_base64}"
                        }
                    ]
                }
            ]
        )

        resultado = resposta.output_text

        if not resultado:
            return "A IA não conseguiu identificar o conteúdo da atividade."

        return resultado

    except Exception as erro:
        traceback.print_exc()
        return f"Erro ao analisar a atividade com IA: {erro}"       

def tela_captura_atividade():
    limpar_principal()
    criar_titulo("📷 Capturar Atividade", "Tire a foto da atividade para correção automática.")

    card = ctk.CTkFrame(principal, fg_color=COR_CARD, corner_radius=18)
    card.pack(fill="both", expand=True, padx=30, pady=20)

    descricao = ctk.CTkLabel(
        card,
        text="Preencha os dados da atividade e capture a imagem. O registro ficará disponível para consulta.",
        font=("Arial", 16),
        text_color=COR_TEXTO_FRACO,
        justify="left"
    )
    descricao.pack(anchor="w", padx=30, pady=(15, 8))

    form = ctk.CTkFrame(card, fg_color="transparent")
    form.pack(fill="x", padx=30, pady=(0, 20))

    entrada_aluno = ctk.CTkEntry(form, placeholder_text="Nome do aluno", width=260, height=40)
    entrada_aluno.grid(row=0, column=0, padx=10, pady=10)
    entrada_disciplina = ctk.CTkEntry(form, placeholder_text="Disciplina", width=260, height=40)
    entrada_disciplina.grid(row=0, column=1, padx=10, pady=10)
    entrada_tipo = ctk.CTkEntry(form, placeholder_text="Tipo de atividade", width=260, height=40)
    entrada_tipo.grid(row=0, column=2, padx=10, pady=10)

    frame_label = ctk.CTkLabel(
        card,
        text="Câmera desligada",
        width=880,
        height=300,
        fg_color="#151f30",
        corner_radius=15,
        font=("Arial", 14),
        text_color=COR_TEXTO,
        justify="center"
    )
    frame_label.pack(fill="x", padx=30, pady=(0, 10))

    resultado_ia = ctk.CTkLabel(
        card,
        text="Resultado da correção automática aparecerá aqui.",
        width=880,
        height=90,
        fg_color="#151f30",
        corner_radius=15,
        font=("Arial", 14),
        text_color=COR_TEXTO,
        justify="left",
        wraplength=860
    )
    resultado_ia.pack(fill="x", padx=30, pady=(0, 10))

    camera_state = {"cap": None, "frame": None, "running": False}

    def atualizar_camera():
        if not camera_state["running"] or camera_state["cap"] is None:
            return

        ret, frame = camera_state["cap"].read()
        if ret:
            camera_state["frame"] = frame
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            imagem_pil = Image.fromarray(frame_rgb).resize((880, 300))
            foto = ImageTk.PhotoImage(imagem_pil)
            frame_label.configure(image=foto, text="")
            frame_label.image = foto

        app.after(30, atualizar_camera)

    def iniciar_camera():
        if camera_state["cap"] is None:
            camera_state["cap"] = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        camera_state["running"] = True
        atualizar_camera()

    def parar_camera():
        camera_state["running"] = False
        if camera_state["cap"] is not None:
            camera_state["cap"].release()
            camera_state["cap"] = None
        frame_label.configure(text="Câmera desligada", image="")
        frame_label.image = None

    def tirar_foto():
        if camera_state["frame"] is None:
            messagebox.showwarning("Atenção", "Abra a câmera primeiro.")
            return

        aluno = entrada_aluno.get().strip() or "Sem nome"
        disciplina = entrada_disciplina.get().strip() or "Sem disciplina"
        tipo_atividade = entrada_tipo.get().strip() or "Sem tipo"

        os.makedirs("atividades", exist_ok=True)
        nome_arquivo = datetime.now().strftime("atividade_%Y%m%d_%H%M%S.jpg")
        caminho = os.path.join("atividades", nome_arquivo)
        cv2.imwrite(caminho, camera_state["frame"])
        parar_camera()

        resultado = corrigir_atividade_com_ia(caminho)
        data_captura = datetime.now().strftime("%d/%m/%Y %H:%M")

        cursor.execute("""
            INSERT INTO atividades (
                aluno,
                disciplina,
                tipo_atividade,
                caminho_imagem,
                resultado,
                nota,
                status,
                data_captura
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            aluno,
            disciplina,
            tipo_atividade,
            caminho,
            resultado,
            None,
            "capturada",
            data_captura
        ))
        conexao.commit()

        resultado_ia.configure(text=resultado)
        messagebox.showinfo("Atividade salva", "Atividade registrada no banco de dados.")
    def selecionar_foto():
        caminho = filedialog.askopenfilename(
            title="Selecionar foto da atividade",
            filetypes=[
                ("Imagens", "*.jpg *.jpeg *.png"),
                ("Todos os arquivos", "*.*")
            ]
        )

        if not caminho:
            return

        try:
            imagem = Image.open(caminho)
            imagem.thumbnail((600, 350))

            foto = ImageTk.PhotoImage(imagem)

            frame_label.configure(image=foto, text="")
            frame_label.image = foto

            resultado = corrigir_atividade_com_ia(caminho)
            resultado_ia.configure(text=resultado)

        except Exception as erro:
            messagebox.showerror(
                "Erro",
                f"Não foi possível processar a imagem:\n{erro}"
            )

    botoes = ctk.CTkFrame(card, fg_color="transparent")
    botoes.pack(fill="x", padx=30, pady=(0, 20))

    ctk.CTkButton(botoes, text="▶ Abrir câmera", width=180, command=iniciar_camera).pack(side="left", padx=10)
    ctk.CTkButton(
    botoes,
    text="📁 Selecionar foto",
    width=180,
    command=selecionar_foto
).pack(side="left", padx=10)
    ctk.CTkButton(botoes, text="📷 Tirar foto", width=180, command=tirar_foto).pack(side="left", padx=10)
    ctk.CTkButton(botoes, text="■ Parar câmera", width=180, command=parar_camera).pack(side="left", padx=10)


def tela_atividades():
    limpar_principal()
    criar_titulo("📚 Atividades", "Consulte atividades registradas no banco de dados.")

    card = ctk.CTkFrame(principal, fg_color=COR_CARD, corner_radius=18)
    card.pack(fill="both", expand=True, padx=30, pady=20)

    estilo = ttk.Style()
    estilo.theme_use("clam")
    estilo.configure(
        "Treeview",
        background="#1f2937",
        foreground="white",
        rowheight=35,
        fieldbackground="#1f2937",
        font=("Arial", 12)
    )
    estilo.configure(
        "Treeview.Heading",
        background=COR_AZUL,
        foreground="white",
        font=("Arial", 12, "bold")
    )

    colunas = ("id", "aluno", "disciplina", "tipo", "data", "status", "resultado", "arquivo")
    tabela = ttk.Treeview(card, columns=colunas, show="headings", height=12)

    tabela.heading("id", text="ID")
    tabela.heading("aluno", text="Aluno")
    tabela.heading("disciplina", text="Disciplina")
    tabela.heading("tipo", text="Tipo")
    tabela.heading("data", text="Data")
    tabela.heading("status", text="Status")
    tabela.heading("resultado", text="Resultado")
    tabela.heading("arquivo", text="Arquivo")

    tabela.column("id", width=50, anchor="center")
    tabela.column("aluno", width=150)
    tabela.column("disciplina", width=140)
    tabela.column("tipo", width=140)
    tabela.column("data", width=130)
    tabela.column("status", width=120, anchor="center")
    tabela.column("resultado", width=300)
    tabela.column("arquivo", width=260)

    tabela.pack(side="left", fill="both", expand=True, padx=(25, 0), pady=25)

    scroll = ttk.Scrollbar(card, orient="vertical", command=tabela.yview)
    scroll.pack(side="right", fill="y", padx=(0, 25), pady=25)
    tabela.configure(yscrollcommand=scroll.set)

    try:
        cursor.execute("""
            SELECT id, aluno, disciplina, tipo_atividade,
                   data_captura, status, resultado, caminho_imagem
            FROM atividades
            ORDER BY id DESC
        """)
        registros = cursor.fetchall()

        for registro in registros:
            tabela.insert("", "end", values=registro)
    except Exception as erro:
        messagebox.showerror("Erro", str(erro))

    def abrir_imagem():
        selecionado = tabela.selection()
        if not selecionado:
            messagebox.showwarning("Atenção", "Selecione uma atividade.")
            return
        valores = tabela.item(selecionado[0], "values")
        caminho = valores[7]
        if not os.path.exists(caminho):
            messagebox.showerror("Erro", "Arquivo de imagem não encontrado.")
            return
        os.startfile(caminho)

    ctk.CTkButton(
        card,
        text="Abrir imagem selecionada",
        width=260,
        command=abrir_imagem
    ).pack(padx=30, pady=(0, 20), anchor="w")
def tela_correcao():
    limpar_principal()

    criar_titulo(
        "☑ Correção",
        "Revise a atividade, atribua a nota e confirme a correção."
    )

    card = ctk.CTkFrame(
        principal,
        fg_color=COR_CARD,
        corner_radius=18
    )
    card.pack(fill="both", expand=True, padx=30, pady=20)

    # -------------------------
    # LISTA DE ATIVIDADES
    # -------------------------

    frame_lista = ctk.CTkFrame(
        card,
        fg_color="transparent"
    )
    frame_lista.pack(fill="x", padx=25, pady=(20, 10))

    ctk.CTkLabel(
        frame_lista,
        text="Selecione uma atividade para corrigir",
        font=("Arial", 18, "bold"),
        text_color=COR_TEXTO
    ).pack(anchor="w", pady=(0, 10))

    atividades = []

    cursor.execute("""
        SELECT id, aluno, disciplina, tipo_atividade, caminho_imagem
        FROM atividades
        ORDER BY id DESC
    """)

    registros = cursor.fetchall()

    for registro in registros:
        id_atividade, aluno, disciplina, tipo, caminho = registro

        atividades.append(
            f"{id_atividade} - {aluno} - {disciplina}"
        )

    if not atividades:
        atividades = ["Nenhuma atividade cadastrada"]

    seletor = ctk.CTkComboBox(
        frame_lista,
        values=atividades,
        width=500,
        height=40
    )
    seletor.pack(anchor="w")

    # -------------------------
    # IMAGEM DA PROVA
    # -------------------------

    imagem_label = ctk.CTkLabel(
        card,
        text="Selecione uma atividade e clique em Visualizar",
        width=600,
        height=280,
        fg_color="#151f30",
        corner_radius=15,
        text_color=COR_TEXTO
    )

    imagem_label.pack(padx=30, pady=15)

    atividade_atual = {
        "id": None,
        "caminho": None
    }

    def visualizar_atividade():

        escolha = seletor.get()

        if escolha == "Nenhuma atividade cadastrada":
            messagebox.showwarning(
                "Atenção",
                "Não existem atividades cadastradas."
            )
            return

        try:
            id_atividade = int(escolha.split(" - ")[0])

            cursor.execute("""
                SELECT caminho_imagem
                FROM atividades
                WHERE id = ?
            """, (id_atividade,))

            registro = cursor.fetchone()

            if not registro:
                messagebox.showerror(
                    "Erro",
                    "Atividade não encontrada."
                )
                return

            caminho = registro[0]

            if not os.path.exists(caminho):
                messagebox.showerror(
                    "Erro",
                    "Imagem da atividade não encontrada."
                )
                return

            atividade_atual["id"] = id_atividade
            atividade_atual["caminho"] = caminho

            imagem = Image.open(caminho)

            imagem.thumbnail((600, 280))

            foto = ImageTk.PhotoImage(imagem)

            imagem_label.configure(
                image=foto,
                text=""
            )

            imagem_label.image = foto

        except Exception as erro:

            messagebox.showerror(
                "Erro",
                str(erro)
            )

    ctk.CTkButton(
        card,
        text="👁 Visualizar atividade",
        width=220,
        command=visualizar_atividade
    ).pack(pady=5)

    # -------------------------
    # RESULTADO
    # -------------------------

    frame_correcao = ctk.CTkFrame(
        card,
        fg_color="transparent"
    )

    frame_correcao.pack(
        fill="x",
        padx=30,
        pady=15
    )

    entrada_resultado = ctk.CTkEntry(
        frame_correcao,
        placeholder_text="Observação / resultado da correção",
        width=500,
        height=40
    )

    entrada_resultado.grid(
        row=0,
        column=0,
        padx=10,
        pady=10
    )

    entrada_nota = ctk.CTkEntry(
        frame_correcao,
        placeholder_text="Nota",
        width=150,
        height=40
    )

    entrada_nota.grid(
        row=0,
        column=1,
        padx=10,
        pady=10
    )

    # -------------------------
    # SALVAR CORREÇÃO
    # -------------------------

    def salvar_correcao():

        if atividade_atual["id"] is None:
            messagebox.showwarning(
                "Atenção",
                "Selecione e visualize uma atividade primeiro."
            )
            return

        resultado = entrada_resultado.get().strip()

        try:
            nota = float(
                entrada_nota.get().replace(",", ".")
            )

        except ValueError:
            messagebox.showerror(
                "Erro",
                "Digite uma nota válida."
            )
            return

        cursor.execute("""
            UPDATE atividades
            SET resultado = ?,
                nota = ?,
                status = ?
            WHERE id = ?
        """, (
            resultado,
            nota,
            "corrigida",
            atividade_atual["id"]
        ))

        conexao.commit()

        messagebox.showinfo(
            "Sucesso",
            "Correção salva com sucesso!"
        )

    ctk.CTkButton(
        card,
        text="💾 Salvar correção",
        width=220,
        height=45,
        fg_color=COR_AZUL,
        font=("Arial", 15, "bold"),
        command=salvar_correcao
    ).pack(pady=10)

def tela_resultados():
    limpar_principal()

    criar_titulo(
        "📊 Resultados",
        "Histórico das médias calculadas."
    )

    card = ctk.CTkFrame(
        principal,
        fg_color=COR_CARD,
        corner_radius=18
    )
    card.pack(fill="both", expand=True, padx=30, pady=20)

    estilo = ttk.Style()
    estilo.theme_use("clam")

    estilo.configure(
        "Treeview",
        background="#1f2937",
        foreground="white",
        rowheight=35,
        fieldbackground="#1f2937",
        font=("Arial", 12)
    )

    estilo.configure(
        "Treeview.Heading",
        background=COR_AZUL,
        foreground="white",
        font=("Arial", 12, "bold")
    )

    colunas = ("nome", "media", "situacao", "faltas", "data")

    tabela = ttk.Treeview(
        card,
        columns=colunas,
        show="headings",
        height=15
    )

    tabela.heading("nome", text="Aluno")
    tabela.heading("media", text="Média")
    tabela.heading("situacao", text="Situação")
    tabela.heading("faltas", text="Faltas")
    tabela.heading("data", text="Data")

    tabela.column("nome", width=250)
    tabela.column("media", width=80, anchor="center")
    tabela.column("situacao", width=220)
    tabela.column("faltas", width=80, anchor="center")
    tabela.column("data", width=160)

    tabela.pack(fill="both", expand=True, padx=25, pady=25)

    try:
        cursor.execute("""
            SELECT nome, media, situacao, faltas, data
            FROM medias_alunos
            ORDER BY id DESC
        """)

        registros = cursor.fetchall()

        for registro in registros:
            nome, media, situacao, faltas, data = registro

            tabela.insert(
                "",
                "end",
                values=(
                    nome,
                    f"{media:.1f}",
                    situacao,
                    faltas,
                    data
                )
            )

    except Exception as erro:
        messagebox.showerror("Erro", str(erro))


def tela_media_aluno():
    limpar_principal()
    criar_titulo("📘 Média do Aluno", "Calcule a média do aluno e verifique a situação.")

    caixa = ctk.CTkFrame(principal, fg_color=COR_CARD, corner_radius=18)
    caixa.pack(fill="both", expand=True, padx=30, pady=20)

    label_dados = ctk.CTkLabel(
        caixa,
        text="1. Informe os dados",
        font=("Arial", 20, "bold"),
        text_color="#60a5fa"
    )
    label_dados.pack(anchor="w", padx=30, pady=(25, 15))

    frame_campos = ctk.CTkFrame(caixa, fg_color="transparent")
    frame_campos.pack(fill="x", padx=30)

    entrada_nome = ctk.CTkEntry(frame_campos, placeholder_text="Nome do aluno", width=300, height=40)
    entrada_nome.grid(row=0, column=0, padx=10, pady=10)

    entrada_nota1 = ctk.CTkEntry(frame_campos, placeholder_text="Nota 1", width=150, height=40)
    entrada_nota1.grid(row=0, column=1, padx=10, pady=10)

    entrada_nota2 = ctk.CTkEntry(frame_campos, placeholder_text="Nota 2", width=150, height=40)
    entrada_nota2.grid(row=0, column=2, padx=10, pady=10)

    entrada_nota3 = ctk.CTkEntry(frame_campos, placeholder_text="Nota 3", width=150, height=40)
    entrada_nota3.grid(row=0, column=3, padx=10, pady=10)

    entrada_faltas = ctk.CTkEntry(frame_campos, placeholder_text="Total de faltas", width=180, height=40)
    entrada_faltas.grid(row=1, column=0, padx=10, pady=10)

    entrada_limite = ctk.CTkEntry(frame_campos, placeholder_text="Limite de faltas", width=180, height=40)
    entrada_limite.grid(row=1, column=1, padx=10, pady=10)

    label_resultado = ctk.CTkLabel(
        caixa,
        text="2. Resultado",
        font=("Arial", 20, "bold"),
        text_color="#60a5fa"
    )
    label_resultado.pack(anchor="w", padx=30, pady=(30, 15))

    frame_resultado = ctk.CTkFrame(caixa, fg_color="transparent")
    frame_resultado.pack(fill="x", padx=30)

    resultado_media = ctk.CTkLabel(
        frame_resultado,
        text="Média Final\n--",
        width=200,
        height=90,
        fg_color="#1e3a8a",
        corner_radius=15,
        font=("Arial", 18, "bold")
    )
    resultado_media.grid(row=0, column=0, padx=10)

    resultado_situacao = ctk.CTkLabel(
        frame_resultado,
        text="Situação\n--",
        width=250,
        height=90,
        fg_color="#065f46",
        corner_radius=15,
        font=("Arial", 18, "bold")
    )
    resultado_situacao.grid(row=0, column=1, padx=10)

    resultado_faltas = ctk.CTkLabel(
        frame_resultado,
        text="Faltas\n--",
        width=200,
        height=90,
        fg_color="#312e81",
        corner_radius=15,
        font=("Arial", 18, "bold")
    )
    resultado_faltas.grid(row=0, column=2, padx=10)

    resultado_limite = ctk.CTkLabel(
        frame_resultado,
        text="Limite\n--",
        width=200,
        height=90,
        fg_color="#78350f",
        corner_radius=15,
        font=("Arial", 18, "bold")
    )
    resultado_limite.grid(row=0, column=3, padx=10)

    def calcular_media():
        try:
            nome = entrada_nome.get()
            nota1 = float(entrada_nota1.get().replace(",", "."))
            nota2 = float(entrada_nota2.get().replace(",", "."))
            nota3 = float(entrada_nota3.get().replace(",", "."))
            faltas = int(entrada_faltas.get())
            limite = int(entrada_limite.get())

            media = (nota1 + nota2 + nota3) / 3

            if faltas > limite:
                situacao = "Compensação de Faltas"
                cor_situacao = "#2563eb"
            elif media >= 6:
                situacao = "✅ Aprovado"
                cor_situacao = "#16a34a"
            else:
                situacao = "❌ Reprovado por Nota"
                cor_situacao = "#dc2626"

            resultado_media.configure(text=f"Média Final\n{media:.1f}")
            resultado_situacao.configure(text=f"Situação\n{situacao}", fg_color=cor_situacao)
            resultado_faltas.configure(text=f"Faltas\n{faltas}")
            resultado_limite.configure(text=f"Limite\n{limite}")

            data_atual = datetime.now().strftime("%d/%m/%Y %H:%M")

            cursor.execute("""
            INSERT INTO medias_alunos (
                nome, nota1, nota2, nota3, media,
                faltas, limite_faltas, situacao, data
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                nome, nota1, nota2, nota3,
                media, faltas, limite, situacao, data_atual
            ))
            conexao.commit()

            messagebox.showinfo("Salvo", "Resultado salvo com sucesso!")

        except Exception:
            messagebox.showerror("Erro", "Preencha todos os campos corretamente.")

    botao = ctk.CTkButton(
        caixa,
        text="🧮 Calcular Média",
        height=45,
        width=250,
        fg_color=COR_AZUL,
        font=("Arial", 16, "bold"),
        command=calcular_media
    )
    botao.pack(pady=35)


# =========================
# MENU LATERAL
# =========================

menu = ctk.CTkFrame(app, width=220, fg_color=COR_MENU, corner_radius=0)
menu.pack(side="left", fill="y")

titulo_menu = ctk.CTkLabel(
    menu,
    text="📋 Sistema de\nCorreção de Notas\nVersão 1.0",
    font=("Arial", 20, "bold"),
    text_color=COR_TEXTO,
    justify="left"
)
titulo_menu.pack(padx=20, pady=30, anchor="w")


def botao_menu(texto, comando):
    return ctk.CTkButton(
        menu,
        text=texto,
        height=48,
        corner_radius=14,
        fg_color="#182449",
        hover_color=COR_HOVER,
        text_color="white",
        font=("Segoe UI", 16, "bold"),
        anchor="w",
        command=comando
    )


botao_menu("🏠 Início", tela_inicio).pack(fill="x", padx=15, pady=5)
botao_menu("📷 Capturar Atividade", tela_captura_atividade).pack(fill="x", padx=15, pady=5)
botao_menu("📚 Atividades", tela_atividades).pack(fill="x", padx=15, pady=5)
botao_menu("📝 Provas", tela_provas).pack(fill="x", padx=15, pady=5)
botao_menu("☑ Correção", tela_correcao).pack(fill="x", padx=15, pady=5)
botao_menu("📊 Resultados", tela_resultados).pack(fill="x", padx=15, pady=5)
botao_menu("📄 Relatórios", lambda: tela_simples("Relatórios")).pack(fill="x", padx=15, pady=5)
botao_menu("👥 Alunos", lambda: tela_simples("Alunos")).pack(fill="x", padx=15, pady=5)
botao_menu("⚙ Configurações", lambda: tela_simples("Configurações")).pack(fill="x", padx=15, pady=5)
botao_menu("🎓 Média do Aluno", tela_media_aluno).pack(fill="x", padx=15, pady=20)

# =========================
# ÁREA PRINCIPAL
# =========================

principal = ctk.CTkFrame(app, fg_color=COR_FUNDO, corner_radius=0)
principal.pack(side="right", fill="both", expand=True)

tela_captura_atividade()

app.mainloop()