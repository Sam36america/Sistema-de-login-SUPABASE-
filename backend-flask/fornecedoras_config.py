# Configuração das fornecedoras de gás
# Cada fornecedora tem seu caminho na rede e o script a ser executado

FORNECEDORAS = {
    'ultragaz': {
        'nome': 'Ultragaz',
        'pasta_base': r'G:\QUALIDADE\Códigos\Leitura de Faturas Gás\Códigos\Ultragaz',
        'pasta_codigo': r'G:\QUALIDADE\Códigos\Leitura de Faturas Gás\Códigos\Ultragaz\Código',
        'pasta_faturas': r'G:\QUALIDADE\Códigos\Leitura de Faturas Gás\Códigos\Ultragaz\Faturas',
        'pasta_lidos': r'G:\QUALIDADE\Códigos\Leitura de Faturas Gás\Códigos\Ultragaz\Lidos',
        'script': 'main_sql.py'
    },
    'comgas': {
        'nome': 'Comgás',
        'pasta_base': r'G:\QUALIDADE\Códigos\Leitura de Faturas Gás\Códigos\Comgás',
        'pasta_codigo': r'G:\QUALIDADE\Códigos\Leitura de Faturas Gás\Códigos\Comgás',
        'pasta_faturas': r'G:\QUALIDADE\Códigos\Leitura de Faturas Gás\Códigos\Comgás\Faturas',
        'pasta_lidos': r'G:\QUALIDADE\Códigos\Leitura de Faturas Gás\Códigos\Comgás\Lidos',
        'script': 'main.py'
    },
    'sulgas': {
        'nome': 'Sulgás',
        'pasta_base': r'G:\QUALIDADE\Códigos\Leitura de Faturas Gás\Códigos\Sulgás',
        'pasta_codigo': r'G:\QUALIDADE\Códigos\Leitura de Faturas Gás\Códigos\Sulgás',
        'pasta_faturas': r'G:\QUALIDADE\Códigos\Leitura de Faturas Gás\Códigos\Sulgás\Faturas',
        'pasta_lidos': r'G:\QUALIDADE\Códigos\Leitura de Faturas Gás\Códigos\Sulgás\Lidos',
        'script': 'main_sql.py'
    },
    'bahiagas': {
        'nome': 'Bahia Gás',
        'pasta_base': r'G:\QUALIDADE\Códigos\Leitura de Faturas Gás\Códigos\Bahia Gás',
        'pasta_codigo': r'G:\QUALIDADE\Códigos\Leitura de Faturas Gás\Códigos\Bahia Gás',
        'pasta_faturas': r'G:\QUALIDADE\Códigos\Leitura de Faturas Gás\Códigos\Bahia Gás\Faturas',
        'pasta_lidos': r'G:\QUALIDADE\Códigos\Leitura de Faturas Gás\Códigos\Bahia Gás\Lidos',
        'script': 'main_sql.py'
    },
    'cegas': {
        'nome': 'Cegás',
        'pasta_base': r'G:\QUALIDADE\Códigos\Leitura de Faturas Gás\Códigos\Cegás',
        'pasta_codigo': r'G:\QUALIDADE\Códigos\Leitura de Faturas Gás\Códigos\Cegás',
        'pasta_faturas': r'G:\QUALIDADE\Códigos\Leitura de Faturas Gás\Códigos\Cegás\Faturas',
        'pasta_lidos': r'G:\QUALIDADE\Códigos\Leitura de Faturas Gás\Códigos\Cegás\Lidos',
        'script': 'main_sql.py'
    },
    'cigas': {
        'nome': 'Cigás',
        'pasta_base': r'G:\QUALIDADE\Códigos\Leitura de Faturas Gás\Códigos\Cigás',
        'pasta_codigo': r'G:\QUALIDADE\Códigos\Leitura de Faturas Gás\Códigos\Cigás',
        'pasta_faturas': r'G:\QUALIDADE\Códigos\Leitura de Faturas Gás\Códigos\Cigás\Faturas',
        'pasta_lidos': r'G:\QUALIDADE\Códigos\Leitura de Faturas Gás\Códigos\Cigás\Lidos',
        'script': 'main_sql.py'
    },
    'compagas': {
        'nome': 'Compagás',
        'pasta_base': r'G:\QUALIDADE\Códigos\Leitura de Faturas Gás\Códigos\Compagás',
        'pasta_codigo': r'G:\QUALIDADE\Códigos\Leitura de Faturas Gás\Códigos\Compagás',
        'pasta_faturas': r'G:\QUALIDADE\Códigos\Leitura de Faturas Gás\Códigos\Compagás\Faturas',
        'pasta_lidos': r'G:\QUALIDADE\Códigos\Leitura de Faturas Gás\Códigos\Compagás\Lidos',
        'script': 'main_sql.py'
    },
    'copergas': {
        'nome': 'Copergás',
        'pasta_base': r'G:\QUALIDADE\Códigos\Leitura de Faturas Gás\Códigos\Copergás',
        'pasta_codigo': r'G:\QUALIDADE\Códigos\Leitura de Faturas Gás\Códigos\Copergás',
        'pasta_faturas': r'G:\QUALIDADE\Códigos\Leitura de Faturas Gás\Códigos\Copergás\Faturas',
        'pasta_lidos': r'G:\QUALIDADE\Códigos\Leitura de Faturas Gás\Códigos\Copergás\Lidos',
        'script': 'main_sql.py'
    },
    'galp': {
        'nome': 'Galp',
        'pasta_base': r'G:\QUALIDADE\Códigos\Leitura de Faturas Gás\Códigos\Galp',
        'pasta_codigo': r'G:\QUALIDADE\Códigos\Leitura de Faturas Gás\Códigos\Galp',
        'pasta_faturas': r'G:\QUALIDADE\Códigos\Leitura de Faturas Gás\Códigos\Galp\Faturas',
        'pasta_lidos': r'G:\QUALIDADE\Códigos\Leitura de Faturas Gás\Códigos\Galp\Lidos',
        'script': 'main_sql.py'
    },
    'gasbrasiliano': {
        'nome': 'Gás Brasiliano',
        'pasta_base': r'G:\QUALIDADE\Códigos\Leitura de Faturas Gás\Códigos\Gás Brasiliano',
        'pasta_codigo': r'G:\QUALIDADE\Códigos\Leitura de Faturas Gás\Códigos\Gás Brasiliano',
        'pasta_faturas': r'G:\QUALIDADE\Códigos\Leitura de Faturas Gás\Códigos\Gás Brasiliano\Faturas',
        'pasta_lidos': r'G:\QUALIDADE\Códigos\Leitura de Faturas Gás\Códigos\Gás Brasiliano\Lidos',
        'script': 'main_sql.py'
    },
    'gaslocal': {
        'nome': 'Gás Local',
        'pasta_base': r'G:\QUALIDADE\Códigos\Leitura de Faturas Gás\Códigos\Gás Local',
        'pasta_codigo': r'G:\QUALIDADE\Códigos\Leitura de Faturas Gás\Códigos\Gás Local',
        'pasta_faturas': r'G:\QUALIDADE\Códigos\Leitura de Faturas Gás\Códigos\Gás Local\Faturas',
        'pasta_lidos': r'G:\QUALIDADE\Códigos\Leitura de Faturas Gás\Códigos\Gás Local\Lidos',
        'script': 'main_sql.py'
    },
    'gasverde': {
        'nome': 'Gás Verde',
        'pasta_base': r'G:\QUALIDADE\Códigos\Leitura de Faturas Gás\Códigos\Gás Verde',
        'pasta_codigo': r'G:\QUALIDADE\Códigos\Leitura de Faturas Gás\Códigos\Gás Verde',
        'pasta_faturas': r'G:\QUALIDADE\Códigos\Leitura de Faturas Gás\Códigos\Gás Verde\Faturas',
        'pasta_lidos': r'G:\QUALIDADE\Códigos\Leitura de Faturas Gás\Códigos\Gás Verde\Lidos',
        'script': 'main_sql.py'
    },
    'gasmig': {
        'nome': 'Gasmig',
        'pasta_base': r'G:\QUALIDADE\Códigos\Leitura de Faturas Gás\Códigos\Gasmig',
        'pasta_codigo': r'G:\QUALIDADE\Códigos\Leitura de Faturas Gás\Códigos\Gasmig',
        'pasta_faturas': r'G:\QUALIDADE\Códigos\Leitura de Faturas Gás\Códigos\Gasmig\Faturas',
        'pasta_lidos': r'G:\QUALIDADE\Códigos\Leitura de Faturas Gás\Códigos\Gasmig\Lidos',
        'script': 'main_sql.py'
    },
    'nacionalgas': {
        'nome': 'Nacional Gás',
        'pasta_base': r'G:\QUALIDADE\Códigos\Leitura de Faturas Gás\Códigos\Nacional Gás',
        'pasta_codigo': r'G:\QUALIDADE\Códigos\Leitura de Faturas Gás\Códigos\Nacional Gás',
        'pasta_faturas': r'G:\QUALIDADE\Códigos\Leitura de Faturas Gás\Códigos\Nacional Gás\Faturas',
        'pasta_lidos': r'G:\QUALIDADE\Códigos\Leitura de Faturas Gás\Códigos\Nacional Gás\Lidos',
        'script': 'main_sql.py'
    },
    'naturgyrj': {
        'nome': 'Naturgy RJ',
        'pasta_base': r'G:\QUALIDADE\Códigos\Leitura de Faturas Gás\Códigos\Naturgy RJ',
        'pasta_codigo': r'G:\QUALIDADE\Códigos\Leitura de Faturas Gás\Códigos\Naturgy RJ',
        'pasta_faturas': r'G:\QUALIDADE\Códigos\Leitura de Faturas Gás\Códigos\Naturgy RJ\Faturas',
        'pasta_lidos': r'G:\QUALIDADE\Códigos\Leitura de Faturas Gás\Códigos\Naturgy RJ\Lidos',
        'script': 'main_sql.py'
    },
    'neogas': {
        'nome': 'Neo Gás',
        'pasta_base': r'G:\QUALIDADE\Códigos\Leitura de Faturas Gás\Códigos\Neo gas',
        'pasta_codigo': r'G:\QUALIDADE\Códigos\Leitura de Faturas Gás\Códigos\Neo gas',
        'pasta_faturas': r'G:\QUALIDADE\Códigos\Leitura de Faturas Gás\Códigos\Neo gas\Faturas',
        'pasta_lidos': r'G:\QUALIDADE\Códigos\Leitura de Faturas Gás\Códigos\Neo gas\Lidos',
        'script': 'main_sql.py'
    },
    'pbgas': {
        'nome': 'PB Gás',
        'pasta_base': r'G:\QUALIDADE\Códigos\Leitura de Faturas Gás\Códigos\PB_Gás',
        'pasta_codigo': r'G:\QUALIDADE\Códigos\Leitura de Faturas Gás\Códigos\PB_Gás',
        'pasta_faturas': r'G:\QUALIDADE\Códigos\Leitura de Faturas Gás\Códigos\PB_Gás\Faturas',
        'pasta_lidos': r'G:\QUALIDADE\Códigos\Leitura de Faturas Gás\Códigos\PB_Gás\Lidos',
        'script': 'main_sql.py'
    },
    'petrobras': {
        'nome': 'Petrobras',
        'pasta_base': r'G:\QUALIDADE\Códigos\Leitura de Faturas Gás\Códigos\Petrobras',
        'pasta_codigo': r'G:\QUALIDADE\Códigos\Leitura de Faturas Gás\Códigos\Petrobras',
        'pasta_faturas': r'G:\QUALIDADE\Códigos\Leitura de Faturas Gás\Códigos\Petrobras\Faturas',
        'pasta_lidos': r'G:\QUALIDADE\Códigos\Leitura de Faturas Gás\Códigos\Petrobras\Lidos',
        'script': 'main_sql.py'
    },
    'potigas': {
        'nome': 'Potigás',
        'pasta_base': r'G:\QUALIDADE\Códigos\Leitura de Faturas Gás\Códigos\Potigás',
        'pasta_codigo': r'G:\QUALIDADE\Códigos\Leitura de Faturas Gás\Códigos\Potigás',
        'pasta_faturas': r'G:\QUALIDADE\Códigos\Leitura de Faturas Gás\Códigos\Potigás\Faturas',
        'pasta_lidos': r'G:\QUALIDADE\Códigos\Leitura de Faturas Gás\Códigos\Potigás\Lidos',
        'script': 'main_sql.py'
    },
    'shell': {
        'nome': 'Shell',
        'pasta_base': r'G:\QUALIDADE\Códigos\Leitura de Faturas Gás\Códigos\Shell',
        'pasta_codigo': r'G:\QUALIDADE\Códigos\Leitura de Faturas Gás\Códigos\Shell',
        'pasta_faturas': r'G:\QUALIDADE\Códigos\Leitura de Faturas Gás\Códigos\Shell\Faturas',
        'pasta_lidos': r'G:\QUALIDADE\Códigos\Leitura de Faturas Gás\Códigos\Shell\Lidos',
        'script': 'main_sql.py'
    }
}
