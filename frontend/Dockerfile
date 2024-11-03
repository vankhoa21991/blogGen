# Dockerfile-frontend

# Imagem base
FROM python:3.9

# Definir o diretório de trabalho no container
WORKDIR /app

ENV FRONTEND_URL='https://bloggen-front-474924334872.europe-west1.run.app'
ENV BACKEND_URL='http://34.91.188.26.nip.io'

# Copiar os arquivos de dependências e instalar
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

# Copiar o restante dos arquivos do projeto
COPY . /app

# Expose port
EXPOSE 8501

# Comando para executar a aplicação
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
