# Flask Monolith Template - Dockerfile
# Imagem base otimizada para Python
FROM python:3.11-slim

# Metadados da imagem
LABEL maintainer="Flask Monolith Template"
LABEL version="1.0.0"
LABEL description="Template completo para aplicações Flask monolíticas"

# Variáveis de ambiente
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    FLASK_APP=app.py \
    FLASK_ENV=production \
    APP_HOST=0.0.0.0 \
    APP_PORT=5000

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libffi-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Criar usuário não-root para segurança
RUN groupadd -r flaskuser && useradd -r -g flaskuser flaskuser

# Definir diretório de trabalho
WORKDIR /app

# Copiar arquivos de dependências
COPY requirements.txt .

# Instalar dependências Python
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copiar código da aplicação
COPY . .

# Criar diretórios necessários
RUN mkdir -p uploads logs instance && \
    chown -R flaskuser:flaskuser /app

# Mudar para usuário não-root
USER flaskuser

# Expor porta da aplicação
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/health || exit 1

# Comando padrão para executar a aplicação
CMD ["python", "app.py"]