import os
import shutil
import pandas as pd
import re
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk

# ===== FUNÇÕES =====

def selecionar_origem():
    pasta = filedialog.askdirectory()
    entry_origem.delete(0, tk.END)
    entry_origem.insert(0, pasta)

def selecionar_destino():
    pasta = filedialog.askdirectory()
    entry_destino.delete(0, tk.END)
    entry_destino.insert(0, pasta)

def selecionar_csv():
    arquivo = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    entry_csv.delete(0, tk.END)
    entry_csv.insert(0, arquivo)

def executar():
    pasta_origem = entry_origem.get()
    pasta_destino = entry_destino.get()
    arquivo_csv = entry_csv.get()
    mes_desejado = combo_mes.get()
    ano_desejado = combo_ano.get()

    if not pasta_origem or not pasta_destino or not arquivo_csv:
        messagebox.showerror("Erro", "Preencha todos os campos!")
        return

    try:
        # ===== LER CSV =====
        df = pd.read_csv(arquivo_csv, sep=";", skiprows=6, encoding="latin1")
        df.columns = df.columns.str.strip()

        df['MATRICULA'] = (
            df['MATRICULA']
            .astype(str)
            .str.extract(r'(\d+)')[0]
        )

        mapa = dict(zip(df['MATRICULA'], df['DATA_ADMISSAO']))

        os.makedirs(pasta_destino, exist_ok=True)

        movidos = 0

        # ===== PROCESSAR =====
        for arquivo in os.listdir(pasta_origem):
            caminho_arquivo = os.path.join(pasta_origem, arquivo)

            if not os.path.isfile(caminho_arquivo):
                continue

            match = re.match(r"(\d+)", arquivo)
            if not match:
                continue

            matricula = match.group(1)

            if matricula not in mapa:
                continue

            data = mapa[matricula]
            if pd.isna(data):
                continue

            data_dt = pd.to_datetime(data, dayfirst=True)

            mes = data_dt.strftime("%m")
            ano = data_dt.strftime("%Y")

            if mes == mes_desejado and ano == ano_desejado:
                destino_final = os.path.join(pasta_destino, arquivo)
                shutil.move(caminho_arquivo, destino_final)
                movidos += 1

        messagebox.showinfo("Sucesso", f"{movidos} arquivos movidos!")

    except Exception as e:
        messagebox.showerror("Erro", str(e))


# ===== INTERFACE =====
janela = tk.Tk()
janela.title("Mover arquivos por mês")
janela.geometry("500x300")

# Origem
tk.Label(janela, text="Pasta de Origem").pack()
entry_origem = tk.Entry(janela, width=50)
entry_origem.pack()
tk.Button(janela, text="Selecionar", command=selecionar_origem).pack()

# Destino
tk.Label(janela, text="Pasta de Destino").pack()
entry_destino = tk.Entry(janela, width=50)
entry_destino.pack()
tk.Button(janela, text="Selecionar", command=selecionar_destino).pack()

# CSV
tk.Label(janela, text="Arquivo CSV").pack()
entry_csv = tk.Entry(janela, width=50)
entry_csv.pack()
tk.Button(janela, text="Selecionar CSV", command=selecionar_csv).pack()

# Mês
tk.Label(janela, text="Mês").pack()
combo_mes = ttk.Combobox(janela, values=[f"{i:02d}" for i in range(1, 13)])
combo_mes.pack()

# Ano (até 2020)
tk.Label(janela, text="Ano").pack()
combo_ano = ttk.Combobox(janela, values=[str(i) for i in range(2026, 2019, -1)])
combo_ano.pack()

# Botão executar
tk.Button(janela, text="Executar", command=executar, bg="green", fg="white").pack(pady=10)

janela.mainloop()
