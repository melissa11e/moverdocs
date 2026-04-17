import os
import shutil
import pandas as pd
import re

# ===== CONFIGURAÇÕES =====
pasta_origem = r"C:\Users\melissa.lemes\OneDrive - HITSS DO BRASIL SERVIÇOS TECNOLOGICOS LTDA\Área de Trabalho\mover contratos\origem"
pasta_destino = r"C:\Users\melissa.lemes\OneDrive - HITSS DO BRASIL SERVIÇOS TECNOLOGICOS LTDA\Área de Trabalho\mover contratos\destino"
arquivo_csv = r"C:\Users\melissa.lemes\OneDrive - HITSS DO BRASIL SERVIÇOS TECNOLOGICOS LTDA\Área de Trabalho\mover contratos\rhfp0773_980329 (6) 1.csv"

# ===== LER CSV =====
df = pd.read_csv(arquivo_csv, sep=";", skiprows=6, encoding="latin1")# ajuste se necessário

# Garantir tipo string
df['MATRICULA'] = df['MATRICULA'].astype(str)

# Criar mapa: matrícula -> data
mapa = dict(zip(df['MATRICULA'], df['DATA_ADMISSAO']))

# ===== PROCESSAR ARQUIVOS =====
for arquivo in os.listdir(pasta_origem):
    caminho_arquivo = os.path.join(pasta_origem, arquivo)

    if not os.path.isfile(caminho_arquivo):
        continue

    try:
        # ===== EXTRAIR MATRÍCULA =====
        match = re.match(r"(\d+)", arquivo)

        if not match:
            print(f"❌ Nome fora do padrão: {arquivo}")
            continue

        matricula = match.group(1)

        # ===== BUSCAR DATA NA PLANILHA =====
        if matricula not in mapa:
            print(f"⚠️ Matrícula não encontrada: {arquivo}")
            continue

        data = mapa[matricula]

        if pd.isna(data):
            print(f"⚠️ Sem data para matrícula {matricula}")
            pasta_mes = "SEM_DATA"
        else:
            # ===== USAR DATA DA PLANILHA =====
            data_dt = pd.to_datetime(data, dayfirst=True)

            # AGRUPAR POR MÊS
            pasta_mes = data_dt.strftime("%Y-%m")

        # ===== DEFINIR CAMINHO FINAL =====
        caminho_pasta_mes = os.path.join(pasta_destino, pasta_mes)

        # ===== CRIAR PASTA SE NÃO EXISTIR =====
        if not os.path.exists(caminho_pasta_mes):
            os.makedirs(caminho_pasta_mes)
            print(f"📁 Pasta criada: {pasta_mes}")

        # ===== MOVER ARQUIVO =====
        destino_final = os.path.join(caminho_pasta_mes, arquivo)
        shutil.move(caminho_arquivo, destino_final)

        print(f"✅ Movido: {arquivo} -> {pasta_mes}")

    except Exception as e:
        print(f"❌ Erro ao processar {arquivo}: {e}")