from flask import Flask, render_template, request, url_for, redirect
import sqlite3
import json
def conecta():
    return sqlite3.connect("Auto_Carros/banco.db")
cursor = conecta()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS conta (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT,
    senha TEXT
    )
""")
cursor.commit()
cursor.close()
app = Flask(__name__)
@app.route("/", methods=["GET", "POST"])
def login():
    paragrafo = None
    if request.method == "POST":
        try:
            email = request.form.get("email")
            senha = request.form.get("senha")
            if not email or not senha:
                paragrafo = "Existem campos vazios"""
            else:
                cursor = conecta()
                verifica = cursor.execute("SELECT * FROM conta WHERE email = ? AND senha = ?", (email, senha)).fetchone()
                cursor.close()
                if verifica[1] == "adm@gmail.com" and verifica[2] == "123":
                    return redirect(url_for("adm"))
                elif verifica[0] != "adm@gmail.com":
                    return redirect(url_for("basico"))
                else:
                    paragrafo = "Conta não encontrada"
        except:
            paragrafo = "Senha ou Email Incorreto"
    return render_template("login.html", p=paragrafo)
@app.route("/cadastro.html", methods=["GET", "POST"])
def cadastro():
    paragrafo = None
    if request.method == "POST":
        email = request.form.get("email")
        senha = request.form.get("senha")
        if not email or not senha:
            paragrafo = "Existem campos vazios"
        else:
            cursor = conecta()
            cursor.execute("INSERT INTO conta (email, senha) VALUES (?, ?)", (email, senha))
            cursor.commit()
            cursor.close()
            return redirect(url_for("login"))
    return render_template("cadastro.html", p=paragrafo)
@app.route("/adm.html", methods=["GET", "POST"])
def adm():
    if request.method == "POST":
        titulo = request.form.get("titulo")
        img = request.files["imagem"]
        video = request.files["video"]
        texto = request.form.get("texto")
        if img and img.filename:
            caminho = "Auto_Carros/static/Image/" + img.filename
            img.save(caminho)
            with open("Auto_Carros/dados.json", "r", encoding="utf-8") as arq:
                dados = json.load(arq)
            dados.append({
                "Título": f"{titulo}",
                "Imagem": "Image/" + img.filename,
                "Texto": f"{texto}"
            })
            with open("Auto_Carros/dados.json", "w", encoding="utf-8") as arquivo:
                    json.dump(dados, arquivo, indent=4, ensure_ascii=False)
        if video and video.filename:
            caminho_video = "Auto_Carros/static/Vid/" + video.filename
            video.save(caminho_video)
            with open("Auto_Carros/dados.json", "r", encoding="utf-8") as arq:
                dados = json.load(arq)
            dados.append({
                "Título": f"{titulo}",
                "Video": "Vid/" + video.filename,
                "Texto": f"{texto}"
            })
            with open("Auto_Carros/dados.json", "w", encoding="utf-8") as arquivo:
                    json.dump(dados, arquivo, indent=4, ensure_ascii=False)
    return render_template("adm.html")
@app.route("/usuario.html", methods=["GET", "POST"])
def basico():
    with open("Auto_Carros/dados.json", "r", encoding="utf-8") as arquivo:
        dados = json.load(arquivo)
    return render_template("usuario.html", dados=dados)
if __name__ == "__main__": 
    app.run(host="0.0.0.0", port=5000)