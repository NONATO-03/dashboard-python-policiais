# Esse arquivo define todas as "rotas", ou seja, as paginas (URLs) da minha aplicação.
# É ele que conecta as ações do usuario no navegador com a logica de dados e os templates HTML.

# Importando as ferramentas do Flask que eu preciso, e tambem o meu modulo de logica de dados (data_handler)
from flask import render_template, request, current_app as app, redirect, url_for, session
from . import data_handler

# Meu dicionario de textos. Deixei tudo aqui para o site poder ser multilingue (portugues e ingles).
# Fica muito mais facil de dar manutençao ou adicionar um novo idioma no futuro.
TEXTS = {
    'pt': {
        'title': 'Análise Quantitativa de Incidentes Envolvendo Forças Policiais',
        'menu_home': 'Início', 'menu_search': 'Pesquisar', 'menu_charts': 'Gráficos',
        'search_title': 'Buscar por ID ou Nome', 'search_placeholder': 'Digite o ID ou nome...',
        'search_button': 'Buscar', 'search_results': 'Resultados da Busca',
        'search_no_results': 'Nenhum resultado encontrado para', 'search_prompt': 'Faça uma busca para ver os resultados.',
        'back_home': 'Voltar para o Início', 'charts_title': 'Mortes por Policiais 🇧🇷',
        'filter_start': 'Data Início:', 'filter_end': 'Data Fim:', 'filter_button': 'Filtrar',
        'filter_clear': 'Limpar Filtro', 'death_manner': 'Tipo de Ocorrência', 'gender': 'Gênero',
        'body_camera': 'Uso de Câmera Corporal', 'threat_level': 'Nível de Ameaça', 'race_bar': 'Raça/Etnia',
        'footer': 'Projeto criado com Flask e Pandas', 'total_deaths': 'Total de Vítimas',
        'last_occurrence': 'Última ocorrência registrada em:', 'us_map': 'Ocorrências por Estado',
        'select_all': 'Selecionar todos', 'deselect_all': 'Desmarcar todos', 'flee': 'Fugiu?',
        'mental': 'Sinais de Distúrbios Mentais?', 'yes': 'Sim', 'no': 'Não', 'true': 'Sim',
        'false': 'Não', 'map_hint': 'Clique nos estados para filtrar', 'armed': 'Arma', 'age': 'Idade',
        'city': 'Cidade','state': 'Estado'
    },
    'en': {
        'title': 'Quantitative Analysis of Police-Involved Incidents',
        'menu_home': 'Home', 'menu_search': 'Search', 'menu_charts': 'Charts',
        'search_title': 'Search by ID or Name', 'search_placeholder': 'Enter ID or name...',
        'search_button': 'Search', 'search_results': 'Search Results',
        'search_no_results': 'No results found for', 'search_prompt': 'Make a search to see results.',
        'back_home': 'Back to Home', 'charts_title': 'Deaths by Police 🇺🇸',
        'filter_start': 'Start Date:', 'filter_end': 'End Date:', 'filter_button': 'Filter',
        'filter_clear': 'Clear Filter', 'death_manner': 'Manner of Death', 'gender': 'Gender',
        'body_camera': 'Body Camera Usage', 'threat_level': 'Threat Level', 'race_bar': 'Race/Ethnicity',
        'footer': 'Project created with Flask and Pandas', 'total_deaths': 'Total victims',
        'last_occurrence': 'Last recorded occurrence:', 'us_map': 'US Map', 'select_all': 'Select all',
        'deselect_all': 'Deselect all', 'flee': 'Flee?', 'mental': 'Mental Disturbance',
        'yes': 'Yes', 'no': 'No', 'true': 'Yes', 'false': 'No', 'map_hint': 'Click states to filter',
        'armed': 'Armed', 'age': 'Age', 'city': 'City', 'state': 'State'
    }
}

# Funçao de ajuda que pega o idioma salvo na sessao do usuario e retorna o dicionario de textos correto.
# Se nao tiver nada, o padrao é portugues.
def get_texts():
    lang = session.get('lang', 'pt')
    return TEXTS.get(lang, TEXTS['pt'])

# Rota para a pagina inicial do projeto (o menu).
@app.route('/')
def home():
    texts = get_texts()
    # Apenas renderiza o template index.html, passando os textos e o idioma atual.
    return render_template('index.html', texts=texts, lang=session.get('lang', 'pt'))

# Rota para a pagina de pesquisa. Ela aceita tanto GET (quando a pagina carrega) quanto POST (quando o formulario de busca é enviado).
@app.route('/pesquisa', methods=['GET', 'POST'])
def pesquisa():
    texts = get_texts()
    search_query = ""
    results = []
    lang = session.get('lang', 'pt')

    # Se a requisição for do tipo POST, significa que o usuario fez uma busca.
    if request.method == 'POST':
        search_query = request.form.get('search_query', '').strip()
        if search_query:
            # Chamo a função de busca do meu data_handler
            results = data_handler.search_data(search_query)
            # Depois de buscar, eu traduzo cada linha do resultado para o idioma correto antes de mostrar na tela
            results = [data_handler.translate_row(row, lang=lang) for row in results]
    
    # Renderizo o template da pagina de pesquisa, passando os resultados e a query (pra ela continuar no campo de busca).
    return render_template('pesquisa.html', results=results, search_query=search_query, texts=texts, lang=lang)

# Essa rota nao é uma pagina, é um 'endpoint' que o formulario de idioma usa.
@app.route('/set_language')
def set_language():
    # Pega o idioma que veio como parametro na URL (ex: /set_language?lang=en)
    lang = request.args.get('lang', 'pt')
    # Salva esse idioma na sessao do usuario, que fica guardada entre as paginas.
    session['lang'] = lang
    # Redireciona o usuario de volta pra pagina onde ele estava.
    next_url = request.referrer or url_for('home')
    return redirect(next_url)

# A rota principal, que mostra o dashboard com os graficos.
@app.route('/graficos')
def graficos():
    texts = get_texts()
    # Primeiro, eu pego todos os parametros de filtro que podem ter vindo na URL (data de inicio, fim e a lista de estados).
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    lang = session.get('lang', 'pt')
    selected_states = request.args.getlist('states') # getlist é importante pra pegar multiplos valores do parametro 'states'.

    # Chamo a função principal do data_handler que me devolve todos os dados ja formatados para os graficos,
    # e tambem as datas minima e maxima do dataset para os limites do filtro.
    chart_data, min_date, max_date = data_handler.get_chart_data(start_date, end_date, lang, selected_states)

    # Se o usuario nao filtrou por data, eu uso as datas min/max como padrao.
    start_date = start_date or min_date
    end_date = end_date or max_date

    # Faço um calculo separado do total de vitimas baseado nos filtros.
    if selected_states and len(selected_states) > 0:
        total_deaths = data_handler.df[data_handler.df['state'].isin(selected_states)].shape[0]
    else:
        total_deaths = data_handler.df.shape[0]
    # E pego a data da ultima ocorrencia para mostrar no rodape.
    last_date = data_handler.df['date'].max().strftime('%d/%m/%Y') if not data_handler.df.empty else '-'

    # Finalmente, renderizo o template dos graficos, passando todas as variaveis que o HTML
    # vai precisar para se construir (dados dos graficos, datas, textos, etc).
    return render_template(
        'graficos.html',
        chart_data=chart_data,
        min_date=min_date,
        max_date=max_date,
        start_date=start_date,
        end_date=end_date,
        texts=texts,
        lang=lang,
        total_deaths=total_deaths,
        last_date=last_date,
        selected_states=selected_states
    )