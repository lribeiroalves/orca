# Estagio de Build
FROM python:3.11-slim AS builder

# Variaveis de ambiente para otimizacao do python
    # PYTHONDONTWRITEBYTECODE=1 evita a criacao de arquivos .pyc desnecessarios
    # PYTHONUNBUFFERED=1 garante que os logs do python apareçam em tempo real no console
ENV PYTHONDONTWRITEBYTECODE=1 
ENV PYTHONUNBUFFERED=1

# Define a pasta de trabalho do container
WORKDIR /app

# Copia apenas os arquivos de dependências (aproveita o cache do Docker)
COPY requirements.txt .

# Instala as dependências no diretório de usuário para copiar facilmente depois
RUN pip install --no-cache-dir --user -r requirements.txt

# --------------------------------------------------------------------------------------------------------------------

# Estagio de Producao
FROM python:3.11-slim AS runner

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Cria um usuário sem privilégios (não-root) por segurança
RUN useradd -u 1001 appuser && chown -R appuser:appuser /app

# Copia as dependências instaladas do estágio de build
COPY --from=builder /root/.local /home/appuser/.local
COPY --from=builder /app /app

# Garante que os executáveis instalados pelo pip fiquem no PATH do novo usuário
ENV PATH=/home/appuser/.local/bin:$PATH

# Copia o código da sua aplicação
COPY . .

# Muda para o usuário não-root
USER appuser

# Porta que a aplicação vai expor
EXPOSE 55000

# Executa o processo usando o formato "exec" (lista)
CMD ["python", "flask", "run"]