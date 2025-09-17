# Importando a classe principal do Flask
from flask import Flask
# Importando a minha classe de configuracao que criei no arquivo config.py
from config import Config

# Essa e a minha 'Application Factory'. Uma função que cria e configura o app.
# Usar esse padrao deixa o projeto mais organizado e facilita testes futuros.
def create_app():
    """
    Cria e configura uma instância da aplicação Flask.
    """
    # Aqui eu crio a instancia principal do Flask.
    # O __name__ ajuda o Flask a saber onde procurar por templates e arquivos estaticos.
    app = Flask(__name__)

    # Carregando as configuracoes do meu arquivo config.py para dentro do app.
    # Coisas como a SECRET_KEY sao carregadas aqui
    app.config.from_object(Config)

    # O 'app_context' garante que a aplicacao esteja 'pronta' antes de eu importar as rotas. é uma boa pratica.
    with app.app_context():
        # Aqui eu importo o arquivo routes.py (o '.' significa do mesmo diretorio),
        # registrando todas as paginas (URLs) que eu defini lá.
        from . import routes

    # Finalmente, a função devolve o app ja criado e configurado, pronto para ser executado pelo run.py
    return app