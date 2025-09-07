# Dockerfile - recomendação para Python 3.13 (imagem oficial slim)
FROM python:3.13-slim

# Metadados opcionais
LABEL maintainer="seu-usuario <seu-email@example.com>"

WORKDIR /app

# Evita prompts interativos e reduz lixo
ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Instala dependências do sistema necessárias (ajuste conforme necessário)
RUN apt-get update \
 && apt-get install -y --no-install-recommends \
    build-essential \
    ca-certificates \
 && rm -rf /var/lib/apt/lists/*

# Copia requirements e instala
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código da aplicação
COPY . .

# Expor porta usada pelo Flask
EXPOSE 5000

# Rodar com gunicorn para produção (2 workers; ajuste conforme necessário)
CMD ["gunicorn", "--workers", "2", "--bind", "0.0.0.0:5000", "app:app"]
