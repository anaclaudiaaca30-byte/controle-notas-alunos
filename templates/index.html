from fastapi import FastAPI, Request, UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import shutil
import qrcode

app = FastAPI()

# Pasta de arquivos estáticos
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):

    # Cria o QR Code
    qr = qrcode.make("http://127.0.0.1:8000/upload")
    qr.save("uploads/qrcode.png")

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "qr_code": "/uploads/qrcode.png"
        }
    )

@app.get("/upload", response_class=HTMLResponse)
async def upload_page():
    return """
    <h2>Enviar Foto da Atividade</h2>

    <form action="/upload" method="post" enctype="multipart/form-data">
        <input type="file" name="arquivo">
        <button type="submit">Enviar</button>
    </form>
    """

@app.post("/upload")
async def upload_file(arquivo: UploadFile = File(...)):

    caminho = f"uploads/{arquivo.filename}"

    with open(caminho, "wb") as buffer:
        shutil.copyfileobj(arquivo.file, buffer)

    return {
        "mensagem": "Foto recebida com sucesso!",
        "arquivo": arquivo.filename
    }