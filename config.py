import os
import secrets

# Criei uma classe 'Config' para guardar todas as minhas variaveis de configuração.
class Config:
    """Configurações base da aplicação Flask."""
    
    # A SECRET_KEY é super importante para a segurança do Flask.
    # Ela protege os dados da sessao do usuario (como o idioma que ele escolheu) e formulários
    #
    # A logica que eu usei foi a seguinte:
    # 1. Ele tenta pegar a chave de uma variavel de ambiente (que é o jeito certo de se fazer em producao)
    # 2. Se nao achar, ele gera uma chave aleatoria e segura na hora. Isso é otimo pro
    #    ambiente de desenvolvimento, porque o app simplesmente funciona sem precisar configurar nada
    SECRET_KEY = os.environ.get('SECRET_KEY') or secrets.token_urlsafe(32)