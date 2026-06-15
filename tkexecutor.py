import customtkinter as ctk
from tkinter import filedialog, messagebox, PhotoImage
import subprocess
import tempfile
import os

ctk.set_appearance_mode("dark")

app = ctk.CTk()

# Define o ícone da janela usando o arquivo PNG em ../icon
icone_path = os.path.join(os.path.dirname(__file__), "..", "icon", "icontkexecutor.png")
if os.path.exists(icone_path):
    app.iconphoto(True, PhotoImage(file=icone_path))

app.title("TkExecutor - Executor de Arquivos Lua e Scripts de Roblox")

largura = 1000
altura = 700

largura_tela = app.winfo_screenwidth()
altura_tela = app.winfo_screenheight()

x = (largura_tela // 2) - (largura // 2)
y = (altura_tela // 2) - (altura // 2)

app.geometry(f"{largura}x{altura}+{x}+{y}")

messagebox.showinfo(
    "TkExecutor",
    "Bem-vindo ao TkExecutor!\n\n"
    "⚠️ IMPORTANTE\n\n"
    "Para executar arquivos .lua, você precisa ter o Interpretador Lua instalado.\n\n"
    "📄 Você pode abrir, editar e salvar arquivos .lua normalmente.\n"
    "▶️ Sem o Interpretador Lua, o botão 'Executar' não funcionará.\n\n"
    "💡 Se aparecer um erro dizendo que 'lua' não foi encontrado, instale o Interpretador Lua primeiro.\n\n"
    "Divirta-se usando o TkExecutor!"
)

arquivo_atual = None

editor = ctk.CTkTextbox(app)
editor.pack(fill="both", expand=True, padx=10, pady=10)

output = ctk.CTkTextbox(app, height=180)
output.pack(fill="x", padx=10, pady=10)

def abrir_arquivo():
    global arquivo_atual

    caminho = filedialog.askopenfilename(
        filetypes=[("Lua Files", "*.lua")]
    )

    if caminho:
        arquivo_atual = caminho

        with open(caminho, "r", encoding="utf-8") as f:
            editor.delete("1.0", "end")
            editor.insert("1.0", f.read())

def salvar_arquivo():
    global arquivo_atual

    if not arquivo_atual:
        arquivo_atual = filedialog.asksaveasfilename(
            defaultextension=".lua",
            filetypes=[("Lua Files", "*.lua")]
        )

    if arquivo_atual:
        with open(arquivo_atual, "w", encoding="utf-8") as f:
            f.write(editor.get("1.0", "end"))

def executar():
    codigo = editor.get("1.0", "end")

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".lua",
        mode="w",
        encoding="utf-8"
    ) as temp:
        temp.write(codigo)
        arquivo_temp = temp.name

    try:
        resultado = subprocess.run(
            ["lua", arquivo_temp],
            capture_output=True,
            text=True
        )

        output.delete("1.0", "end")

        texto = ""

        if resultado.stdout:
            texto += resultado.stdout

        if resultado.stderr:
            texto += "\n" + resultado.stderr

        output.insert("1.0", texto)

    except Exception as erro:
        output.delete("1.0", "end")
        output.insert("1.0", str(erro))

    finally:
        os.remove(arquivo_temp)

barra = ctk.CTkFrame(app)
barra.pack(fill="x")

ctk.CTkButton(
    barra,
    text="Abrir .lua",
    command=abrir_arquivo
).pack(side="left", padx=5, pady=5)

ctk.CTkButton(
    barra,
    text="Salvar",
    command=salvar_arquivo
).pack(side="left", padx=5, pady=5)

ctk.CTkButton(
    barra,
    text="Executar",
    command=executar
).pack(side="left", padx=5, pady=5)

app.mainloop()