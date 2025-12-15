from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import sys
from datetime import datetime
from pathlib import Path
import threading
import uuid

# Adicionar pasta scripts ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'scripts'))

from scripts.main_sql import main as processar_fatura
from scripts.sql_functions import buscar_id_cliente, buscar_id_fornecedor
from scripts.models import DatabaseConfig
import pyodbc
import subprocess
from fornecedoras_config import FORNECEDORAS

# Cache global para armazenar status dos processamentos
processing_status = {}

app = Flask(__name__)
# Configurar CORS para permitir requisições do Vercel e ngrok
CORS(app, resources={
    r"/api/*": {
        "origins": "*",
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization", "ngrok-skip-browser-warning"],
        "expose_headers": ["Content-Type"],
        "supports_credentials": False
    }
})

# Configurações
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
TEMP_FOLDER = os.path.join(os.path.dirname(__file__), 'temp')
PROCESSED_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads', 'Lidos')
ALLOWED_EXTENSIONS = {'pdf', 'xml'}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(TEMP_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return jsonify({
        'message': 'API de Leitura de Faturas - Vora Energia',
        'version': '1.0.0',
        'status': 'online'
    })

@app.route('/api/health', methods=['GET'])
def health_check():
    """Verifica se a API e banco estão funcionando"""
    try:
        db_config = DatabaseConfig()
        conn = pyodbc.connect(db_config.connection_string)
        conn.close()
        return jsonify({
            'status': 'healthy',
            'database': 'connected',
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'database': 'disconnected',
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

@app.route('/api/upload', methods=['POST'])
def upload_file():
    """Recebe arquivos PDF ou XML para processamento"""
    if 'file' not in request.files:
        return jsonify({'error': 'Nenhum arquivo enviado'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'Nome de arquivo vazio'}), 400

    if not allowed_file(file.filename):
        return jsonify({'error': 'Tipo de arquivo não permitido. Use PDF ou XML'}), 400

    try:
        # Salvar arquivo temporariamente
        filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{file.filename}"
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)

        return jsonify({
            'message': 'Arquivo enviado com sucesso',
            'filename': filename,
            'filepath': filepath,
            'size': os.path.getsize(filepath)
        }), 200

    except Exception as e:
        return jsonify({'error': f'Erro ao salvar arquivo: {str(e)}'}), 500

@app.route('/api/processar', methods=['POST'])
def processar():
    """Processa um arquivo de fatura"""
    data = request.get_json()

    if not data or 'filepath' not in data:
        return jsonify({'error': 'Caminho do arquivo não fornecido'}), 400

    filepath = data['filepath']

    if not os.path.exists(filepath):
        return jsonify({'error': 'Arquivo não encontrado'}), 404

    try:
        # Processar o arquivo usando o script existente
        diretorio_origem = os.path.dirname(filepath)
        resultado = processar_fatura(diretorio_origem, filepath, PROCESSED_FOLDER)

        return jsonify({
            'message': 'Arquivo processado com sucesso',
            'resultado': resultado,
            'timestamp': datetime.now().isoformat()
        }), 200

    except Exception as e:
        return jsonify({
            'error': f'Erro ao processar arquivo: {str(e)}',
            'timestamp': datetime.now().isoformat()
        }), 500

@app.route('/api/faturas', methods=['GET'])
def listar_faturas():
    """Lista faturas processadas no banco de dados"""
    try:
        db_config = DatabaseConfig()
        conn = pyodbc.connect(db_config.connection_string)
        cursor = conn.cursor()

        # Query para listar faturas (últimas 50)
        query = """
        SELECT TOP 50
            ID_FATURA,
            VALOR_NF,
            VOLUME,
            DATA_EMISSAO,
            NUM_NF,
            ICMS,
            CNPJ_CLIENTE,
            FORNECEDOR,
            INICIO_FORNECIMENTO,
            FIM_FORNECIMENTO
        FROM tb_faturas_combustiveis_teste
        ORDER BY DATA_EMISSAO DESC
        """

        cursor.execute(query)
        rows = cursor.fetchall()

        faturas = []
        for row in rows:
            faturas.append({
                'id': row[0],
                'valor': float(row[1]) if row[1] else 0,
                'volume': float(row[2]) if row[2] else 0,
                'data_emissao': row[3].isoformat() if row[3] else None,
                'numero_nf': row[4],
                'icms': float(row[5]) if row[5] else 0,
                'cnpj_cliente': row[6],
                'fornecedor': row[7],
                'inicio_fornecimento': row[8].isoformat() if row[8] else None,
                'fim_fornecimento': row[9].isoformat() if row[9] else None
            })

        conn.close()

        return jsonify({
            'faturas': faturas,
            'total': len(faturas),
            'timestamp': datetime.now().isoformat()
        }), 200

    except Exception as e:
        return jsonify({
            'error': f'Erro ao buscar faturas: {str(e)}',
            'timestamp': datetime.now().isoformat()
        }), 500

@app.route('/api/clientes', methods=['GET'])
def listar_clientes():
    """Lista clientes cadastrados"""
    try:
        db_config = DatabaseConfig()
        conn = pyodbc.connect(db_config.connection_string)
        cursor = conn.cursor()

        query = "SELECT ID_CLIENTE, CNPJ, NOME FROM tb_cliente WHERE ID_CLIENTE > 0"
        cursor.execute(query)
        rows = cursor.fetchall()

        clientes = []
        for row in rows:
            clientes.append({
                'id': row[0],
                'cnpj': row[1],
                'nome': row[2] if len(row) > 2 else 'N/A'
            })

        conn.close()

        return jsonify({
            'clientes': clientes,
            'total': len(clientes)
        }), 200

    except Exception as e:
        return jsonify({'error': f'Erro ao buscar clientes: {str(e)}'}), 500

@app.route('/api/fornecedores', methods=['GET'])
def listar_fornecedores():
    """Lista fornecedores cadastrados"""
    try:
        db_config = DatabaseConfig()
        conn = pyodbc.connect(db_config.connection_string)
        cursor = conn.cursor()

        query = "SELECT ID_FORNECEDOR, FORNECEDOR FROM tb_fornecedor_combustiveis WHERE ID_FORNECEDOR > 0"
        cursor.execute(query)
        rows = cursor.fetchall()

        fornecedores = []
        for row in rows:
            fornecedores.append({
                'id': row[0],
                'nome': row[1]
            })

        conn.close()

        return jsonify({
            'fornecedores': fornecedores,
            'total': len(fornecedores)
        }), 200

    except Exception as e:
        return jsonify({'error': f'Erro ao buscar fornecedores: {str(e)}'}), 500

@app.route('/api/fornecedoras', methods=['GET'])
def listar_fornecedoras():
    """Lista fornecedoras de gás disponíveis para processamento"""
    try:
        fornecedoras_list = []
        for key, config in FORNECEDORAS.items():
            fornecedoras_list.append({
                'id': key,
                'nome': config['nome'],
                'pasta_base': config['pasta_base']
            })

        return jsonify({
            'fornecedoras': fornecedoras_list,
            'total': len(fornecedoras_list)
        }), 200

    except Exception as e:
        return jsonify({'error': f'Erro ao listar fornecedoras: {str(e)}'}), 500

def executar_processamento(job_id, fornecedora_id, config):
    """Executa o processamento de uma fornecedora em thread separada"""
    try:
        # Caminho completo do script
        script_path = os.path.join(config['pasta_codigo'], config['script'])
        python_exe = sys.executable

        # Adicionar log inicial
        processing_status[job_id]['logs'].append(f"🚀 Iniciando processamento de {config['nome']}...")
        processing_status[job_id]['logs'].append(f"📁 Script: {script_path}")

        # Executar processo
        process = subprocess.Popen(
            [python_exe, script_path],
            cwd=config['pasta_codigo'],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,  # Line buffered
            universal_newlines=True
        )

        # Ler linha por linha em tempo real
        for line in process.stdout:
            line = line.strip()
            if line:
                processing_status[job_id]['logs'].append(line)

        # Aguardar conclusão
        return_code = process.wait(timeout=300)  # 5 min timeout

        # Atualizar status final
        if return_code == 0:
            processing_status[job_id].update({
                'status': 'completed',
                'end_time': datetime.now(),
                'error': None
            })
            processing_status[job_id]['logs'].append(f"✅ Processamento concluído com sucesso!")
        else:
            processing_status[job_id].update({
                'status': 'error',
                'end_time': datetime.now(),
                'error': f'Processo retornou código de erro: {return_code}'
            })
            processing_status[job_id]['logs'].append(f"❌ Erro: Processo retornou código {return_code}")

    except subprocess.TimeoutExpired:
        process.kill()
        processing_status[job_id].update({
            'status': 'error',
            'end_time': datetime.now(),
            'error': 'Timeout: processamento excedeu 5 minutos'
        })
        processing_status[job_id]['logs'].append('❌ Erro: Timeout - processamento excedeu 5 minutos')

    except Exception as e:
        processing_status[job_id].update({
            'status': 'error',
            'end_time': datetime.now(),
            'error': str(e)
        })
        processing_status[job_id]['logs'].append(f'❌ Erro: {str(e)}')

@app.route('/api/processar-fornecedora/<fornecedora_id>', methods=['POST'])
def processar_fornecedora(fornecedora_id):
    """Inicia o processamento assíncrono de uma fornecedora específica"""
    try:
        # Verificar se a fornecedora existe
        if fornecedora_id not in FORNECEDORAS:
            return jsonify({'error': f'Fornecedora {fornecedora_id} não encontrada'}), 404

        config = FORNECEDORAS[fornecedora_id]

        # Verificar se as pastas existem
        if not os.path.exists(config['pasta_codigo']):
            return jsonify({'error': f'Pasta de código não encontrada: {config["pasta_codigo"]}'}), 404

        if not os.path.exists(config['pasta_faturas']):
            return jsonify({'error': f'Pasta de faturas não encontrada: {config["pasta_faturas"]}'}), 404

        # Caminho completo do script
        script_path = os.path.join(config['pasta_codigo'], config['script'])

        if not os.path.exists(script_path):
            return jsonify({'error': f'Script não encontrado: {script_path}'}), 404

        # Gerar job_id único
        job_id = str(uuid.uuid4())

        # Inicializar status no cache
        processing_status[job_id] = {
            'fornecedora_id': fornecedora_id,
            'fornecedora_nome': config['nome'],
            'status': 'processing',
            'logs': [],
            'start_time': datetime.now(),
            'end_time': None,
            'error': None
        }

        # Executar processamento em thread separada
        thread = threading.Thread(
            target=executar_processamento,
            args=(job_id, fornecedora_id, config)
        )
        thread.daemon = True
        thread.start()

        # Retornar job_id imediatamente
        return jsonify({
            'job_id': job_id,
            'fornecedora': config['nome'],
            'message': 'Processamento iniciado'
        }), 202  # 202 Accepted

    except Exception as e:
        return jsonify({
            'error': f'Erro ao processar fornecedora: {str(e)}',
            'timestamp': datetime.now().isoformat()
        }), 500

@app.route('/api/status-processamento/<job_id>', methods=['GET'])
def status_processamento(job_id):
    """Retorna o status atual e logs de um processamento"""
    if job_id not in processing_status:
        return jsonify({'error': 'Job não encontrado'}), 404

    job = processing_status[job_id]

    return jsonify({
        'job_id': job_id,
        'fornecedora_id': job['fornecedora_id'],
        'fornecedora_nome': job['fornecedora_nome'],
        'status': job['status'],
        'logs': job['logs'],
        'start_time': job['start_time'].isoformat(),
        'end_time': job['end_time'].isoformat() if job['end_time'] else None,
        'error': job['error']
    }), 200

if __name__ == '__main__':
    print('🚀 Iniciando API Flask - Vora Energia')
    print(f'📁 Pasta de uploads: {UPLOAD_FOLDER}')
    print(f'🔧 Ambiente: Desenvolvimento')
    app.run(host='0.0.0.0', port=5000, debug=True)
