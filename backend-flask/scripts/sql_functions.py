import os
import PyPDF2
import re
import pyodbc
import shutil
import pandas as pd
from models import *
from datetime import datetime, timedelta, date
from decimal import Decimal, InvalidOperation
from config import *
import numpy as np
from calendar import monthrange
import calendar

def verificar_duplicata_sql(connection_string, informacoes):
    """
    Verifica se já existe um registro com os mesmos dados no banco SQL.
    Retorna True se encontrar duplicata, False caso contrário.
    """
    import pyodbc
    
    try:
        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()
        
        # Campos para verificar duplicata
        cnpj = informacoes.get('cnpj', '')
        data_inicio = informacoes.get('data_inicio')
        data_fim = informacoes.get('data_fim')
        valor_total = informacoes.get('valor_total')
        
        # Query para verificar duplicata
        query = """
        SELECT COUNT(*) FROM tb_faturas_combustiveis_teste 
        WHERE CNPJ_CLIENTE = ? AND INICIO_FORNECIMENTO = ? AND FIM_FORNECIMENTO = ? AND VALOR_NF = ?
        """
        
        cursor.execute(query, [cnpj, data_inicio, data_fim, valor_total])
        count = cursor.fetchone()[0]
        conn.close()
        
        if count > 0:
            print(f"[DUPLICATA SQL] Encontrada: CNPJ={cnpj}, Período={data_inicio} a {data_fim}, Valor={valor_total}")
            return True
        else:
            print(f"[DEBUG] Nenhuma duplicata SQL encontrada para CNPJ={cnpj}")
            return False
            
    except Exception as e:
        print(f"[ERRO] Erro ao verificar duplicata no SQL: {e}")
        return False  # Em caso de erro, permite inserção

def safe_decimal(valor):
    """
    Converte string de valor monetário brasileiro ou padrão para Decimal corretamente.
    Exemplo: '11.659,50' -> Decimal('11659.50'), '11659.50' -> Decimal('11659.50')
    """
    if valor is None:
        return Decimal('0.00')
    if isinstance(valor, Decimal):
        return valor
    if isinstance(valor, (int, float)):
        return Decimal(str(valor))
    valor = str(valor).strip()
    # Se vier do XML já como 11659.50, só converte
    if valor.count('.') == 1 and valor.count(',') == 0:
        try:
            return Decimal(valor)
        except InvalidOperation:
            pass
    # Se vier como 11.659,50 (padrão brasileiro)
    if ',' in valor:
        partes = valor.split(',')
        inteiro = partes[0].replace('.', '')
        decimal = partes[1]
        valor = f"{inteiro}.{decimal}"
    else:
        # Se não tem vírgula, mas tem mais de um ponto, provavelmente é milhar brasileiro
        if valor.count('.') > 1:
            valor = valor.replace('.', '')
        # Se não tem vírgula nem múltiplos pontos, deixa como está
    try:
        return Decimal(valor)
    except (ValueError, InvalidOperation):
        print(f"[ERRO] Valor inválido para Decimal: {valor}")
        return Decimal('0.00')

def parse_date(value):
    """
    🔧 CORRIGIDO: Converte um valor para datetime.date SEM forçar último dia.
    Retorna None se inválido para que seja tratado posteriormente.
    """
    if not value or str(value).strip().lower() in ['none', '', 'null']:
        return None  # 🔧 MUDANÇA: Retorna None em vez de último dia

    if isinstance(value, date):
        return value
    
    if isinstance(value, datetime):
        return value.date()

    if isinstance(value, str):
        for fmt in ('%Y-%m-%d', '%d/%m/%Y', '%Y/%m/%d', '%d-%m-%Y'):
            try:
                return datetime.strptime(value.strip(), fmt).date()
            except ValueError:
                continue

    return None  # 🔧 MUDANÇA: Retorna None em vez de último dia

def inserir_dados_no_sql(connection_string, informacoes, distribuidora):
    try:
        # ✅ VERIFICAR DUPLICATA ANTES DE INSERIR
        if verificar_duplicata_sql(connection_string, informacoes):
            print(f"❌ Registro duplicado encontrado no SQL. Não será inserido.")
            return "duplicado"
        
        # 🔧 CORRIGIDO: Converter datas SEM alterar valores válidos
        data_emissao = parse_date(informacoes.get('data_emissao'))
        data_inicio = parse_date(informacoes.get('data_inicio'))
        data_fim = parse_date(informacoes.get('data_fim'))

        print(f"[DEBUG SQL] Datas após parse_date:")
        print(f"  - Data emissão: {data_emissao}")
        print(f"  - Data início: {data_inicio}")
        print(f"  - Data fim: {data_fim}")

        # 🔧 NOVO: Criar datas padrão apenas se AMBAS forem None (caso PDF)
        if data_inicio is None and data_fim is None and data_emissao:
            print(f"[INFO SQL] PDF detectado - criando datas baseadas na emissão: {data_emissao}")
            
            ano = data_emissao.year
            mes = data_emissao.month
            
            # Data início = primeiro dia do mês
            data_inicio = date(ano, mes, 1)
            print(f"[INFO SQL] Data início criada: {data_inicio}")
            
            # Data fim = último dia do mês
            ultimo_dia = monthrange(ano, mes)[1]
            data_fim = date(ano, mes, ultimo_dia)
            print(f"[INFO SQL] Data fim criada: {data_fim}")
            
        elif data_inicio is None or data_fim is None:
            print(f"[ERRO SQL] Datas incompletas: início={data_inicio}, fim={data_fim}")
            return False

        # Verificar se temos todas as datas obrigatórias
        if not data_emissao or not data_inicio or not data_fim:
            print(f"[ERRO SQL] Datas obrigatórias ausentes: emissão={data_emissao}, início={data_inicio}, fim={data_fim}")
            return False

        print(f"[DEBUG SQL] Datas finais para inserção:")
        print(f"  - Data emissão: {data_emissao}")
        print(f"  - Data início: {data_inicio}")
        print(f"  - Data fim: {data_fim}")

        # Garantir que valores numéricos estejam no formato correto
        informacoes['valor_total'] = safe_decimal(informacoes.get('valor_total'))
        informacoes['volume_total'] = safe_decimal(informacoes.get('volume_total'))
        informacoes['valor_icms'] = safe_decimal(informacoes.get('valor_icms'))

        # Garantir que CNPJ seja uma string válida
        informacoes['cnpj'] = str(informacoes.get('cnpj')).strip()

        # Buscar IDs necessários
        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()

        # Buscar ID do Cliente
        query_cliente = "SELECT ID_CLIENTE FROM tb_cliente WHERE CNPJ = ?"
        cursor.execute(query_cliente, informacoes['cnpj'])
        result_cliente = cursor.fetchone()
        if result_cliente:
            id_cliente = result_cliente[0]
            print(f"[DEBUG SQL] ID_CLIENTE encontrado: {id_cliente}")
        else:
            print(f"[ERRO SQL] ID_CLIENTE não encontrado para CNPJ: {informacoes['cnpj']}")
            conn.close()
            return False

        # Buscar ID do Fornecedor
        query_fornecedor = "SELECT ID_FORNECEDOR FROM tb_fornecedor_combustiveis WHERE FORNECEDOR = ?"
        cursor.execute(query_fornecedor, distribuidora)
        result_fornecedor = cursor.fetchone()
        if result_fornecedor:
            id_fornecedor = result_fornecedor[0]
            print(f"[DEBUG SQL] ID_FORNECEDOR encontrado: {id_fornecedor}")
        else:
            print(f"[ERRO SQL] ID_FORNECEDOR não encontrado para distribuidora: {distribuidora}")
            conn.close()
            return False

        # Montar a query de inserção
        query = '''
            INSERT INTO tb_faturas_combustiveis_teste (
                VALOR_NF, VOLUME, DATA_EMISSAO, NUM_NF, ICMS,
                CNPJ_CLIENTE, FORNECEDOR, INICIO_FORNECIMENTO, FIM_FORNECIMENTO,
                ID_CLIENTE, ID_FORNECEDOR
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        '''
        
        # 🔧 USAR AS DATAS TRATADAS LOCALMENTE
        params = [
            informacoes['valor_total'],
            informacoes['volume_total'],
            data_emissao,          # Usar variável local
            informacoes.get('numero_fatura'),
            informacoes['valor_icms'],
            informacoes['cnpj'],
            distribuidora,
            data_inicio,           # Usar variável local
            data_fim,              # Usar variável local
            id_cliente,
            id_fornecedor
        ]

        print(f"[DEBUG SQL] Parâmetros para inserção:")
        print(f"  - Valor: {params[0]}")
        print(f"  - Volume: {params[1]}")
        print(f"  - Data emissão: {params[2]}")
        print(f"  - Data início: {params[7]}")
        print(f"  - Data fim: {params[8]}")

        if any(param is None for param in params):
            print(f"[ERRO SQL] Parâmetros inválidos detectados: {params}")
            return False

        try:
            cursor.execute(query, params)
            conn.commit()
            print("[INFO SQL] Dados inseridos com sucesso no banco de dados.")
            return True
        except pyodbc.Error as e:
            print(f"[ERRO SQL] Falha ao inserir dados no SQL: {e}")
            return False

    except Exception as e:
        print(f"[ERRO SQL] Ocorreu um erro inesperado: {e}")
        return False
    finally:
        if 'conn' in locals() and conn:
            conn.close()

def buscar_id_cliente(connection_string, cnpj_cliente):
    try:
        # Conectar ao banco de dados
        conn = pyodbc.connect(connection_string)

        # Consulta SQL para buscar o nome do fornecedor
        query = '''
            SELECT ID_CLIENTE, CNPJ
            FROM tb_cliente
            WHERE CNPJ = ?
        '''

        # Executando a consulta com pandas
        df_cliente = pd.read_sql(query, conn, params=[cnpj_cliente])

        # Fechar a conexão
        conn.close()

        # Verificar se há resultados
        if not df_cliente.empty:
            # Pegamos todos os valores da coluna ID_CLIENTE
            id_list = df_cliente['ID_CLIENTE'].tolist()

            # Removemos qualquer ID igual a 0
            id_list = [id for id in id_list if id != 0]

            if id_list:
                id_cliente = int(id_list[0])  # Pegamos o primeiro valor válido
            else:
                id_cliente = None  # Se não sobrar nenhum ID válido
            print(f"[DEBUG] ID_CLIENTE selecionado: {id_cliente}")
            return id_cliente  # Retorna o ID_CLIENTE encontrado
        else:
            print("Nenhum Cliente encontrado.")
            return None

    except Exception as e:
        print(f"Erro ao buscar cliente: {e}")
        return None

def buscar_id_fornecedor(connection_string, fornecedor):
    try:
        # Conectar ao banco de dados
        conn = pyodbc.connect(connection_string)

        # Consulta SQL para buscar o ID do fornecedor
        query = '''
            SELECT ID_FORNECEDOR
            FROM tb_fornecedor_combustiveis
            WHERE FORNECEDOR = ?
        '''

        # Executando a consulta com pandas
        df_fornecedor = pd.read_sql(query, conn, params=[fornecedor])

        # Fechar a conexão
        conn.close()

        # Verificar se há resultados
        if not df_fornecedor.empty:
            # Pegamos todos os valores da coluna ID_FORNECEDOR
            id_list = df_fornecedor['ID_FORNECEDOR'].tolist()

            # Removemos qualquer ID igual a 0
            id_list = [id for id in id_list if id != 0]

            if id_list:
                id_fornecedor = int(id_list[0])  # Pegamos o primeiro valor válido
            else:
                id_fornecedor = None  # Se não sobrar nenhum ID válido
            print(f"[DEBUG] ID_FORNECEDOR selecionado: {id_fornecedor}")
            return id_fornecedor  # Retorna o ID_FORNECEDOR encontrado
        else:
            print(f"Nenhum Fornecedor encontrado para: {fornecedor}")
            return None

    except Exception as e:
        print(f"Erro ao buscar fornecedor: {e}")
        return None