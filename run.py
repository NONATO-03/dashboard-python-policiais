# Este é o script principal para iniciar a aplicação.
# É so rodar 'python run.py' no terminal que tudo começa a funcionar
from app import create_app
import webbrowser
from threading import Timer

# Aqui eu chamo a minha 'Application Factory' para criar a instancia do app ja configurada
app = create_app()

# Criei essa função simples so pra abrir o navegador na pagina certa.
def open_browser():
    """
    Abre o navegador na URL da aplicação.
    """
    webbrowser.open_new('http://127.0.0.1:5000/')

# Esse bloco garante que o código aqui dentro só vai rodar quando eu executar o arquivo diretamente (python run.py)
# e nao se ele for importado por outro arquivo.
if __name__ == '__main__':
    # Um truque que adicionei para melhorar a experiencia do usuario.
    # isso aqui agenda a abertura automatica do navegador 1 segundo depois do servidor começar a rodar.
    Timer(1, open_browser).start()
    
    # E aqui é o comando que de fato inicia o servidor de desenvolvimento do Flask.
    # O 'debug=True' é uma mao na roda durante o desenvolvimento, ele mostra erros detalhados
    # e reinicia o servidor sozinho quando eu mudo o codigo. Mas nunca se deve usar isso em produção...
    # Coloquei 'use_reloader=False' por um motivo especifico: com o debug ativado, o Flask
    # tende a rodar o script duas vezes, o que faria o navegador abrir duas vezes.
    # Desativando isso, garanto que ele abra só uma vez 
    app.run(debug=True, use_reloader=False)