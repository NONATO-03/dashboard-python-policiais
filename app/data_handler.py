# Esse arquivo é o "cérebro" do meu projeto.
# Toda a logica de carregar os dados do CSV, limpar, filtrar e preparar para os graficos fica aqui.

# Importando as bibliotecas que eu preciso. Pandas é a principal para manipular os dados
import pandas as pd
from matplotlib import cm
import numpy as np

# FUNÇÕES AUXILIARES DE CORES 

# Uma função de ajuda pra gerar cores bonitas para os graficos
# Eu pego um 'colormap' do Matplotlib e gero uma lista de cores em formato RGBA que o Chart.js entende.
def get_colors(n, colormap_name='viridis'):
    """Gera uma lista de N cores RGBA a partir de um colormap do Matplotlib."""
    colormap = cm.get_cmap(colormap_name)
    colors = colormap(np.linspace(0.2, 0.8, n))
    return [f'rgba({int(r*255)}, {int(g*255)}, {int(b*255)}, 0.75)' for r, g, b, a in colors]

# CARREGAMENTO E PREPARAÇÃO DOS DADOS

# O bloco principal de carregamento de dados.
# Coloquei um try-except pra evitar que o app quebre se o arquivo CSV não for encontrado.
try:
    # Lendo o arquivo CSV com o pandas. O encoding 'latin-1' resolveu problemas com caracteres especiais.
    df = pd.read_csv('Deaths_by_Police_US.csv', encoding='latin-1')
    
    # Faço uma limpeza inicial nos dados aqui:
    # 1. Converte a coluna de data para o formato datetime do pandas. 'coerce' transforma datas invalidas em Nulo.
    df['date'] = pd.to_datetime(df['date'], format='%d/%m/%y', errors='coerce')
    # 2. Remove qualquer linha que tenha ficado com a data nula.
    df.dropna(subset=['date'], inplace=True)
    # 3. Garante que os IDs sejam tratados como texto.
    df['id'] = df['id'].astype(str)
    # 4. Remove espaços em branco extras dos nomes.
    df['name'] = df['name'].str.strip()
    # 5. Preenche valores vazios em colunas importantes com 'Unknown' pra nao dar problema nas contagens.
    for col in ['race', 'manner_of_death', 'threat_level', 'flee', 'body_camera']:
        df[col] = df[col].fillna('Unknown')
except FileNotFoundError:
    print("Erro: O arquivo 'Deaths_by_Police_US.csv' não foi encontrado.")
    # Se o arquivo nao existir, crio um DataFrame vazio para o app nao quebrar
    df = pd.DataFrame()

# DICIONÁRIOS DE TRADUÇÃO CENTRALIZADOS

# Essa função é a minha central de traduções
# Deixei todos os textos que precisam ser traduzidos aqui, separados por idioma. Fica muito mais facil de dar manutenção.
def get_translation_dicts(lang='pt'):
    if lang == 'en':
        # Dicionarios para o ingles
        return {
            'manner_labels': {'shot': 'Shot', 'shot and Tasered': 'Shot and Tasered', 'Unknown': 'Unknown'},
            'race_labels': {'W': 'White', 'B': 'Black', 'H': 'Hispanic', 'A': 'Asian', 'N': 'Native American', 'O': 'Other', 'Unknown': 'Unknown'},
            'gender_labels': {'M': 'Male', 'F': 'Female', 'Unknown': 'Unknown'},
            'body_camera_labels': {'TRUE': 'Yes', 'FALSE': 'No', 'true': 'Yes', 'false': 'No', True: 'Yes', False: 'No', 'Unknown': 'Unknown'},
            'threat_labels': {'attack': 'Attack', 'other': 'Other', 'undetermined': 'Undetermined', 'Unknown': 'Unknown'},
            'flee_map': {'Not fleeing': 'Not fleeing', 'Car': 'Car', 'Foot': 'On foot', 'Other': 'Other', 'Unknown': 'Unknown', '': 'Unknown', None: 'Unknown'},
            'mental_map': {True: 'Yes', False: 'No', 'TRUE': 'Yes', 'FALSE': 'No', 'True': 'Yes', 'False': 'No', 'Yes': 'Yes', 'No': 'No', 'Unknown': 'Unknown', '': 'Unknown', None: 'Unknown'}
        }
    else:
        # Dicionarios para o portugues (padrão)
        return {
            'manner_labels': {'shot': 'Tiro', 'shot and Tasered': 'Tiro e Taser', 'Unknown': 'Desconhecido'},
            'race_labels': {'W': 'Branco', 'B': 'Negro', 'H': 'Hispânico', 'A': 'Asiático', 'N': 'Nativo Americano', 'O': 'Outro', 'Unknown': 'Desconhecido'},
            'gender_labels': {'M': 'Masculino', 'F': 'Feminino', 'Unknown': 'Desconhecido'},
            'body_camera_labels': {'TRUE': 'Sim', 'FALSE': 'Não', 'true': 'Sim', 'false': 'Não', True: 'Sim', False: 'Não', 'Unknown': 'Desconhecido'},
            'threat_labels': {'attack': 'Ataque', 'other': 'Outro', 'undetermined': 'Indeterminado', 'Unknown': 'Desconhecido'},
            'flee_map': {'Not fleeing': 'Não fugiu', 'Car': 'Carro', 'Foot': 'A pé', 'Other': 'Outro', 'Unknown': 'Desconhecido', '': 'Desconhecido', None: 'Desconhecido'},
            'mental_map': {True: 'Sim', False: 'Não', 'TRUE': 'Sim', 'FALSE': 'Não', 'True': 'Sim', 'False': 'Não', 'Yes': 'Sim', 'No': 'Não', 'Unknown': 'Desconhecido', '': 'Desconhecido', None: 'Desconhecido'}
        }

# FUNÇÃO PARA TRADUZIR UMA LINHA DE RESULTADO 

# Uma função mais especifica para traduzir uma unica linha de resultado.
# Eu uso ela na pagina de pesquisa para mostrar os dados no idioma certo.
def translate_row(row, lang='pt'):
    """Traduz campos específicos de uma linha de resultado conforme o idioma."""
    dicts = get_translation_dicts(lang)
    row = row.copy()
    # Para cada campo, eu pego o valor traduzido do dicionario. Se nao achar, mantenho o original.
    if 'gender' in row: row['gender'] = dicts['gender_labels'].get(row['gender'], row['gender'])
    if 'body_camera' in row: row['body_camera'] = dicts['body_camera_labels'].get(row['body_camera'], row['body_camera'])
    if 'signs_of_mental_illness' in row: row['signs_of_mental_illness'] = dicts['mental_map'].get(row['signs_of_mental_illness'], row['signs_of_mental_illness'])
    if 'manner_of_death' in row: row['manner_of_death'] = dicts['manner_labels'].get(row['manner_of_death'], row['manner_of_death'])
    if 'race' in row: row['race'] = dicts['race_labels'].get(row['race'], row['race'])
    if 'threat_level' in row: row['threat_level'] = dicts['threat_labels'].get(row['threat_level'], row['threat_level'])
    if 'flee' in row: row['flee'] = dicts['flee_map'].get(row['flee'], row['flee'])
    return row

# FUNÇÕES DE LÓGICA DE DADOS 
# A logica da minha ferramenta de pesquisa.
def search_data(query):
    """
    Busca no DataFrame por ID ou por nome (case-insensitive).
    Retorna uma lista de dicionários com os resultados.
    """
    if df.empty or not query:
        return []
    # O filtro do pandas procura o 'query' tanto na coluna de ID quanto na de nome.
    # O 'case=False' faz com que a busca nao diferencie maiusculas de minusculas.
    result_df = df[
        df['id'].str.contains(query, case=False, na=False) |
        df['name'].str.contains(query, case=False, na=False)
    ]
    # Retorno os resultados como uma lista de dicionarios, que é um formato facil de usar no template HTML.
    return result_df.to_dict('records')

# Essa é a função mais importante, o motor do meu dashboard
# Ela recebe os filtros (data, idioma, estados) e prepara todos os dados para os graficos.
def get_chart_data(start_date=None, end_date=None, lang='pt', selected_states=None):
    if df.empty:
        return {}, '', '' # Retorna vazio se nao conseguiu carregar o CSV

    # Começo com o DataFrame completo e vou aplicando os filtros.
    filtered_df = df
    # 1. Filtro por data
    if start_date and end_date:
        start_date = pd.to_datetime(start_date, format='%Y-%m-%d')
        end_date = pd.to_datetime(end_date, format='%Y-%m-%d')
        filtered_df = filtered_df[(filtered_df['date'] >= start_date) & (filtered_df['date'] <= end_date)]
    # 2. Filtro por estados selecionados no mapa
    if selected_states and len(selected_states) > 0:
        filtered_df = filtered_df[filtered_df['state'].isin(selected_states)]

    # Pego o dicionario de traducoes correto para o idioma selecionado
    dicts = get_translation_dicts(lang)

    # Para facilitar a criacao dos graficos ja no idioma certo, eu crio colunas novas no DataFrame
    # (ex: 'race_pt') com os valores já traduzidos, usando o metodo .map().
    filtered_df = filtered_df.copy()
    filtered_df['manner_of_death_pt'] = filtered_df['manner_of_death'].map(dicts['manner_labels']).fillna(filtered_df['manner_of_death'])
    filtered_df['race_pt'] = filtered_df['race'].map(dicts['race_labels']).fillna(filtered_df['race'])
    filtered_df['gender_pt'] = filtered_df['gender'].map(dicts['gender_labels']).fillna(filtered_df['gender'])
    filtered_df['body_camera_pt'] = filtered_df['body_camera'].map(dicts['body_camera_labels']).fillna(filtered_df['body_camera'])
    filtered_df['threat_level_pt'] = filtered_df['threat_level'].map(dicts['threat_labels']).fillna(filtered_df['threat_level'])

    charts = {}

    # Criei essa função interna como uma 'fabrica de graficos'.
    # Ela pega uma serie de dados, conta os valores, pega as cores e monta o objeto JSON certinho que o Chart.js precisa.
    # Isso evitou um monte de codigo repetido.
    def create_chart_json(data_series, chart_type, colormap='viridis'):
        counts = data_series.value_counts()
        labels = counts.index.tolist()
        values = counts.values.tolist()
        background_color = get_colors(len(labels), colormap_name=colormap)
        return {
            'labels': labels,
            'datasets': [{
                'label': data_series.name.replace('_pt', '').replace('_', ' ').title(),
                'data': values,
                'backgroundColor': background_color,
                'borderColor': [color.replace('0.75', '1') for color in background_color],
                'borderWidth': 1
            }]
        }

    # Aqui eu monto o dicionario final com os dados de todos os graficos,
    # chamando a minha 'fabrica' para cada um deles com um colormap diferente.
    charts['manner_of_death'] = create_chart_json(filtered_df['manner_of_death_pt'], 'bar', colormap='plasma')
    charts['gender'] = create_chart_json(filtered_df['gender_pt'], 'pie', colormap='cool')
    charts['body_camera'] = create_chart_json(filtered_df['body_camera_pt'], 'pie', colormap='inferno')
    charts['threat_level'] = create_chart_json(filtered_df['threat_level_pt'], 'bar', colormap='magma')
    charts['race_bar'] = create_chart_json(filtered_df['race_pt'], 'bar', colormap='viridis')

    # Para os graficos de 'fuga' e 'doença mental', o tratamento é um pouco diferente
    # porque os dados originais sao mais bagunçados. Eu mapeio eles primeiro para padronizar.
    flee_series = filtered_df['flee'].map(dicts['flee_map']).fillna(dicts['flee_map'].get('Unknown', 'Unknown'))
    charts['flee'] = create_chart_json(flee_series, 'bar', colormap='cubehelix')

    mental_series = filtered_df['signs_of_mental_illness'].map(dicts['mental_map']).fillna(dicts['mental_map'].get('Unknown', 'Unknown'))
    charts['signs_of_mental_illness'] = create_chart_json(mental_series, 'bar', colormap='coolwarm')

    # Pego a data minima e maxima do DataFrame completo para usar nos limites do filtro de data
    min_date = df['date'].min().strftime('%Y-%m-%d')
    max_date = df['date'].max().strftime('%Y-%m-%d')

    # A função retorna tudo que a pagina de graficos precisa.
    return charts, min_date, max_date