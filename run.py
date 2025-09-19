# Importa a função que cria nossa aplicação
from app import create_app

# Cria a instância da aplicação que o Gunicorn vai usar
app = create_app()

# O código abaixo só será usado se você rodar 'python run.py' localmente
if __name__ == '__main__':
    app.run(debug=True)
