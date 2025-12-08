import logging
import re
class DatabaseConfig:
    def __init__(self):
        self.server = 'gestaodb2.americaenergia.com.br'
        self.database = 'america_gestao'
        self.username = 'america_gestao'
        self.password = 'HTHhdt6352s!23'
        self.connection_string = ( 
            f'DRIVER={{MySQL ODBC 8.0 Unicode Driver}};'
            f'SERVER={self.server};'
            f'PORT=3306;'
            f'DATABASE={self.database};'
            f'UID={self.username};'
            f'PWD={self.password};'
            f'OPTION=3;'
        )

class ExtratorFaturas:
    def __init__(self):
        self.regexes = {
            'cnpj': [r'(\d{2}\.\d+\.\d+\/\d+\-?\d+)DATA'], # 
            'valor_total': [r'PRODUTOS\s?(\d+\.?\,?\d+\.?\,?\d+?\.?\,?\d+?\.?\,?)'], # 
            'volume_total': [r'QUIDO\s?(\d+\.?\,?\d+\,?\.?\d+)'], 
            'data_emissao': [r'EMISSÃO\s?(\d+\/\d+\/\d+)'], 
            'data_inicio': [r''], 
            'data_fim': [r''],

            'numero_fatura': [r'Nº\s?(\d+\.\d+\.\d+)', #24/07
                             r'\s(\d+)\s?\SÉRIE?'], 

            'valor_icms': [r'ICMS\s(\d+\.?\,?\d+)']   
        }

    def extrair_informacoes(self, texto):
        informacoes = {}
        for chave, regex_list in self.regexes.items():
            for regex in regex_list:
                match = re.search(regex, texto)
                if match:
                    informacoes[chave] = match.group(1) if match.groups() else match.group(0)
                    break  # Para de procurar assim que encontrar uma correspondência
            if chave not in informacoes:
                print(f"Valor não encontrado para: {chave}")
                informacoes[chave] = None  # Define como None se algum valor não for encontrado
        return informacoes