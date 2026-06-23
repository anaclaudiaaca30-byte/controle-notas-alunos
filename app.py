from fastapi import FastAPI, Request, UploadFile, File, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import shutil
import qrcode
import sqlite3
import os
from datetime import datetime

app = FastAPI()

# Cria pasta uploads se não existir
os.makedirs("uploads", exist_ok=True)

# Arquivos estáticos
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

templates = Jinja2Templates(directory="templates")


# ==========================
# BANCO DE DADOS
# ==========================

def criar_banco():
    conexao = sqlite3.connect("alunos.db")
    cursor = conexao.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS envios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            turma TEXT,
            bimestre TEXT,
            arquivo TEXT,
            data_envio TEXT
        )
    """)

    conexao.commit()
    conexao.close()

criar_banco()


# ==========================
# PÁGINA INICIAL
# ==========================

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):

    qr = qrcode.make("http://127.0.0.1:8000/upload")
    qr.save("uploads/qrcode.png")

    return templates.TemplateResponse(
        request,
        "index.html",
        {
            "qr_code": "/uploads/qrcode.png"
        }
    )


# ==========================
# TELA DE ENVIO
# ==========================

@app.get("/upload", response_class=HTMLResponse)
async def upload_page():

    return """
    <h1>Enviar Atividade</h1>

    <form action="/upload" method="post" enctype="multipart/form-data">

        <label>Nome do aluno:</label><br>
        <input type="text" name="nome" required><br><br>

        <label>Turma:</label><br>
        <input type="text" name="turma" required><br><br>

        <label>Bimestre:</label><br>
        <input type="text" name="bimestre" required><br><br>

        <label>Foto da atividade:</label><br>
        <input type="file" name="arquivo" required><br><br>

        <button type="submit">Enviar Atividade</button>

    </form>

    <br>
    <a href="/">Voltar</a>
    """


# ==========================
# SALVAR ENVIO
# ==========================

@app.post("/upload")
async def upload_file(
    nome: str = Form(...),
    turma: str = Form(...),
    bimestre: str = Form(...),
    arquivo: UploadFile = File(...)
):

    caminho = f"uploads/{arquivo.filename}"

    with open(caminho, "wb") as buffer:
        shutil.copyfileobj(arquivo.file, buffer)

    data_envio = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    conexao = sqlite3.connect("alunos.db")
    cursor = conexao.cursor()

    cursor.execute("""
        INSERT INTO envios
        (nome, turma, bimestre, arquivo, data_envio)
        VALUES (?, ?, ?, ?, ?)
    """,
    (
        nome,
        turma,
        bimestre,
        arquivo.filename,
        data_envio
    ))

    conexao.commit()
    conexao.close()

    return HTMLResponse(f"""
        <h2>Atividade enviada com sucesso!</h2>

        <p><b>Aluno:</b> {nome}</p>
        <p><b>Turma:</b> {turma}</p>
        <p><b>Bimestre:</b> {bimestre}</p>
        <p><b>Arquivo:</b> {arquivo.filename}</p>

        <br>

        <a href="/upload">Enviar outra atividade</a>

        <br><br>

        <a href="/alunos">Ver alunos cadastrados</a>
    """)


# ==========================
# LISTAR ALUNOS
# ==========================

@app.get("/alunos", response_class=HTMLResponse)
async def listar_alunos():

    conexao = sqlite3.connect("alunos.db")
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT
        id,
        nome,
        turma,
        bimestre,
        arquivo,
        data_envio
        FROM envios
    """)

    alunos = cursor.fetchall()

    conexao.close()

    html = """
    <h1>Alunos Cadastrados</h1>

    <table border='1' cellpadding='8'>
        <tr>
            <th>ID</th>
            <th>Nome</th>
            <th>Turma</th>
            <th>Bimestre</th>
            <th>Arquivo</th>
            <th>Data</th>
            <th>Foto</th>
        </tr>
    """

    for aluno in alunos:

        html += f"""
        <tr>
            <td>{aluno[0]}</td>
            <td>{aluno[1]}</td>
            <td>{aluno[2]}</td>
            <td>{aluno[3]}</td>
            <td>{aluno[4]}</td>
            <td>{aluno[5]}</td>
            <td>
                <a href="/uploads/{aluno[4]}" target="_blank">
                    Abrir Foto
                </a>
            </td>
        </tr>
        """

    html += """
    </table>

    <br><br>

    <a href="/">Página Inicial</a>
    """

    return HTMLResponse(html)
# ==========================
# GABARITO DA ATIVIDADE
# ==========================

@app.get("/gabarito", response_class=HTMLResponse)
async def pagina_gabarito():
    return """
    <h1>Cadastrar Gabarito</h1>

    <form action="/gabarito" method="post">

        <label>Questão 1:</label><br>
        <input type="text" name="q1"><br><br>

        <label>Questão 2:</label><br>
        <input type="text" name="q2"><br><br>

        <label>Questão 3:</label><br>
        <input type="text" name="q3"><br><br>

        <label>Questão 4:</label><br>
        <input type="text" name="q4"><br><br>

        <label>Questão 5:</label><br>
        <input type="text" name="q5"><br><br>

        <button type="submit">Salvar Gabarito</button>
    </form>

    <br>
    <a href="/">Voltar</a>
    """


@app.post("/gabarito")
async def salvar_gabarito(
    q1: str = Form(""),
    q2: str = Form(""),
    q3: str = Form(""),
    q4: str = Form(""),
    q5: str = Form("")
):
    conexao = sqlite3.connect("alunos.db")
    cursor = conexao.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS gabarito (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            q1 TEXT,
            q2 TEXT,
            q3 TEXT,
            q4 TEXT,
            q5 TEXT,
            data_cadastro TEXT
        )
    """)

    data_cadastro = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    cursor.execute("""
        INSERT INTO gabarito (q1, q2, q3, q4, q5, data_cadastro)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (q1, q2, q3, q4, q5, data_cadastro))

    conexao.commit()
    conexao.close()

    return HTMLResponse("""
    <h2>Gabarito salvo com sucesso!</h2>
    <a href="/gabarito">Cadastrar outro gabarito</a><br>
    <a href="/">Voltar para página inicial</a>
    """)
@app.get("/corrigir", response_class=HTMLResponse)
async def pagina_corrigir():
    return """
    <h1>Correção da Atividade</h1>

    <form action="/corrigir" method="post">

        <label>Resposta Questão 1:</label><br>
        <input type="text" name="q1"><br><br>

        <label>Resposta Questão 2:</label><br>
        <input type="text" name="q2"><br><br>

        <label>Resposta Questão 3:</label><br>
        <input type="text" name="q3"><br><br>

        <label>Resposta Questão 4:</label><br>
        <input type="text" name="q4"><br><br>

        <label>Resposta Questão 5:</label><br>
        <input type="text" name="q5"><br><br>

        <button type="submit">Corrigir</button>

    </form>

    <br>
    <a href="/">Voltar</a>
    """
@app.post("/corrigir")
async def corrigir(
    q1: str = Form(""),
    q2: str = Form(""),
    q3: str = Form(""),
    q4: str = Form(""),
    q5: str = Form("")
):
    conexao = sqlite3.connect("alunos.db")
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT q1, q2, q3, q4, q5
        FROM gabarito
        ORDER BY id DESC
        LIMIT 1
    """)

    gabarito = cursor.fetchone()
    conexao.close()

    respostas = [q1, q2, q3, q4, q5]
    acertos = 0

    for resposta, correta in zip(respostas, gabarito):
        if resposta.strip().lower() == correta.strip().lower():
            acertos += 1

    nota = round((acertos / 5) * 10, 2)

    if nota >= 6:
        situacao = "APROVADO"
        compensacao = "NÃO"
    else:
        situacao = "RECUPERAÇÃO"
        compensacao = "SIM"

    return HTMLResponse(f"""
    <h1>Resultado</h1>
    <p><b>Acertos:</b> {acertos}/5</p>
    <p><b>Nota:</b> {nota}</p>
    <p><b>Situação:</b> {situacao}</p>
    <p><b>Compensação de Falta:</b> {compensacao}</p>
    <br>
    <a href="/corrigir">Corrigir outro aluno</a>
    """)