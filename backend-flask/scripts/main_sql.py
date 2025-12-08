import os
import PyPDF2
import re
import pyodbc
import shutil
from datetime import datetime, timedelta
from calendar import monthrange
from xml.etree import ElementTree as ET
from models import *
from config import *
from functions import * 
from sql_functions import *

def main(file_path, arquivo, diretorio_destino=None):
    informacoes = None

    # Se não for fornecido diretório de destino, usa a mesma pasta do arquivo
    if diretorio_destino is None:
        diretorio_destino = file_path

    # Verifica se o arquivo é XML
    if arquivo.lower().endswith('.xml'):
        try:
            tree = ET.parse(arquivo)
            root = tree.getroot()
            informacoes = extrair_informacoes_xml(root)
        except Exception as e:
            print(f"❌ Erro ao processar o XML: {arquivo} - {e}")
            return

    # Verifica se o arquivo é PDF
    elif arquivo.lower().endswith('.pdf'):
        texto_pypdf = extrair_texto(arquivo)
        if not texto_pypdf:
            print(f"❌ Falha na extração de texto do PDF: {arquivo}")
            return

        # Extrai informações com a classe ExtratorFaturas
        informacoes_config = ExtratorFaturas()
        informacoes = informacoes_config.extrair_informacoes(texto_pypdf)
        if not informacoes or all(v is None for v in informacoes.values()):
            print(f"❌ Nenhuma informação útil extraída do PDF: {arquivo}")
            return

        # Extrai o número da fatura no padrão "Nº 000.001.479"
        informacoes["numero_fatura"] = extrair_numero_fatura_limpo(texto_pypdf)

    else:
        print(f"⚠️ Formato de arquivo não suportado: {arquivo}")
        return

    # Normaliza o CNPJ ANTES de tratar datas
    if informacoes is not None:
        cnpj = informacoes.get('cnpj')
        if cnpj is not None:
            informacoes['cnpj'] = re.sub(r'[^\d]', '', str(cnpj))
        else:
            informacoes['cnpj'] = ''
        
        # 🔧 AJUSTE: Tratar datas ANTES de verificar duplicatas e inserir no banco
        print(f"[DEBUG] Datas antes do tratamento: início={informacoes.get('data_inicio')}, fim={informacoes.get('data_fim')}")
        informacoes = tratar_datas(informacoes)
        print(f"[DEBUG] Datas após tratamento: início={informacoes.get('data_inicio')}, fim={informacoes.get('data_fim')}")

        # ✅ VERIFICAR SE ARQUIVO JÁ EXISTE NO DESTINO (após ter todas as datas)
        nome_arquivo = os.path.basename(arquivo)
        destino = os.path.join(diretorio_destino, nome_arquivo)
        
        if os.path.exists(destino):
            print(f"⚠️ Arquivo já existe no destino. Excluindo arquivo original: {arquivo}")
            excluir_arquivo(arquivo)
            return

        # Insere no banco de dados (agora com datas completas)
        db_config = DatabaseConfig()
        sucesso_insercao = inserir_dados_no_sql(db_config.connection_string, informacoes, DIST)

        if sucesso_insercao == "duplicado":
            print(f"⚠️ Entrada duplicada detectada. Excluindo arquivo: {arquivo}")
            excluir_arquivo(arquivo)
        elif sucesso_insercao:
            try:
                mover_arquivo(arquivo, diretorio_destino)
                print(f"📁 Arquivo movido para: {diretorio_destino}")
            except Exception as e:
                print(f"❌ Erro ao mover arquivo: {e}")
        else:
            print(f"📄 Arquivo mantido na pasta original devido a falha na inserção: {arquivo}")

# Caminhos de origem e destino (comentado - agora controlado pela API Flask)
# diretorio_origem = r'G:\QUALIDADE\Códigos\Leitura de Faturas Gás\Códigos\Ultragaz\Faturas'
# diretorio_destino = r'G:\QUALIDADE\Códigos\Leitura de Faturas Gás\Códigos\Ultragaz\Lidos'

# Processar os arquivos na pasta de origem (comentado - agora controlado pela API Flask)
# for arquivo in os.listdir(diretorio_origem):
#     if arquivo.lower().endswith(('.pdf', '.xml')):
#         main(diretorio_origem, os.path.join(diretorio_origem, arquivo))