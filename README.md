# ORCA

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python 3.11+" />
  <img src="https://img.shields.io/badge/Flask-3.x-000000?style=for-the-badge&logo=flask&logoColor=white" alt="Flask" />
  <img src="https://img.shields.io/badge/SQLite-Local-5BC0DE?style=for-the-badge&logo=sqlite&logoColor=white" alt="SQLite" />
  <img src="https://img.shields.io/badge/Docker-Deploy-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="Docker" />
</p>

Sistema de gestão financeira pessoal para controlar entradas, saídas, saldos, faturas, compras parceladas e relatórios financeiros.

## Guias de referência

- [README-PT-BR-compact.md](README-PT-BR-compact.md) — versão enxuta em português
- [README-EN.md](README-EN.md) — versão em inglês

## 🚀 Guia de uso rápido (do zero)

Se você acabou de clonar o repositório em uma máquina nova, siga este fluxo exato:

```bash
git clone <url-do-repositorio>
cd orca
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip pip-tools
pip-compile requirements.in
pip install -r requirements.txt
mkdir -p instance
cp .env.example .env
make run
```

A aplicação ficará disponível em:

```text
http://127.0.0.1:5000
```

> Importante: o arquivo `.env` deve apontar para uma pasta local válida. Para testes locais, o recomendado é usar SQLite em `instance/database.db`.

## 📁 Arquivos locais não versionados

Os itens abaixo são locais da máquina do desenvolvedor e não devem ser enviados ao Git:

- `.env`
- `.venv/`
- `instance/`
- `instance/database.db`
- `config/secrets.toml`
- caches e arquivos gerados em execução local

O projeto já inclui [.gitignore](.gitignore) para impedir que esses arquivos entrem no controle de versão.

## 🔧 Troubleshooting rápido

### `make run` falha com `flask: No such file or directory`

Isso acontece quando o ambiente virtual não foi criado ou não foi ativado. Use:

```bash
python3 -m venv .venv
source .venv/bin/activate
make run
```

### Banco não encontrado / erro de conexão

Verifique se o `.env` contém um caminho válido para o SQLite, por exemplo:

```env
DYNACONF_SQLALCHEMY_DATABASE_URI=sqlite:////home/seu-usuario/orca/instance/database.db
```

E confirme que a pasta existe:

```bash
mkdir -p instance
```

### Migração não é aplicada

Ao iniciar a aplicação, o projeto tenta aplicar as migrações automaticamente. Se isso não acontecer, execute manualmente:

```bash
source .venv/bin/activate
flask --app app db upgrade
```

## 📌 Visão geral

O ORCA é uma aplicação web em Flask para gestão doméstica e financeira pessoal. O projeto foi estruturado com foco em simplicidade de desenvolvimento, modularização e deploy automatizado.

### Principais recursos
- cadastro de usuários;
- registro de entradas e saídas;
- gestão de saldos por banco e período;
- controle de faturas e compras parceladas;
- visualização de dados em tabelas e gráficos;
- administração via Flask-Admin;
- suporte a SQLite em desenvolvimento local;
- deploy automatizado com Docker e GitHub Actions.

## 🧱 Stack

- Python 3.11
- Flask
- SQLAlchemy
- Flask-Migrate
- Flask-WTF
- Flask-Admin
- Dynaconf
- Alembic
- Babel
- SQLite
- Docker
- pip-tools

## 🗂️ Estrutura do projeto

```text
orca/
├── app/
│   ├── blueprint/
│   │   └── webui/
│   ├── ext/
│   │   ├── admin/
│   │   ├── configuration/
│   │   ├── database/
│   │   └── migration/
│   ├── seeders/
│   ├── static/
│   └── templates/
├── config/
│   └── settings.toml
├── instance/
├── migrations/
├── .github/workflows/deploy.yml
├── .env.example
├── .gitignore
├── .dockerignore
├── dockerfile
├── Makefile
├── requirements.in
├── requirements.txt
├── README.md
├── README-PT-BR-compact.md
├── README-EN.md
├── LICENSE
└── ...
```

## ⚙️ Requisitos

- Python 3.11+
- Git
- pip
- virtualenv
- Docker (opcional para deploy)

## 🚀 Setup local

### 1) Clone o repositório

```bash
git clone <url-do-repositorio>
cd orca
```

### 2) Crie o ambiente virtual

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3) Instale as dependências

```bash
python -m pip install --upgrade pip pip-tools
pip-compile requirements.in
pip install -r requirements.txt
```

Ou use o atalho do projeto:

```bash
make requirements
```

### 4) Prepare o arquivo `.env`

Crie um arquivo `.env` na raiz do projeto:

```env
FLASK_APP=app
FLASK_ENV=development
FLASK_RUN_HOST=0.0.0.0
FLASK_RUN_PORT=5000
FLASK_DEBUG=1
DYNACONF_SECRET_KEY=troque-por-uma-chave-forte
DYNACONF_SQLALCHEMY_DATABASE_URI=sqlite:////absolute/path/to/orca/instance/database.db
```

Exemplo prático:

```env
FLASK_APP=app
FLASK_ENV=development
FLASK_RUN_HOST=0.0.0.0
FLASK_RUN_PORT=5000
FLASK_DEBUG=1
DYNACONF_SECRET_KEY=minha-chave-local
DYNACONF_SQLALCHEMY_DATABASE_URI=sqlite:////home/seu-usuario/orca/instance/database.db
```

Crie também a pasta de persistência:

```bash
mkdir -p instance
```

## ▶️ Executando localmente

```bash
make run
```

A aplicação iniciará em:

```text
http://127.0.0.1:5000
```

## 🧪 SQLite para testes locais

Para desenvolvimento e testes locais, o projeto foi pensado para usar SQLite com o caminho:

```text
instance/database.db
```

Esse é o modo mais simples para rodar a aplicação em um clone novo e validar o comportamento sem necessidade de MySQL ou outro banco externo.

## 🧬 Migrações e banco de dados

O projeto usa Flask-Migrate/Alembic para versionamento do banco.

### Comandos úteis

```bash
flask --app app db migrate -m "mensagem"
flask --app app db upgrade
```

As migrações são aplicadas automaticamente quando a aplicação inicia, conforme a lógica implementada em:

- [app/ext/migration/__init__.py](app/ext/migration/__init__.py)
- [config/settings.toml](config/settings.toml)

## 🏗️ Arquitetura

### Extensões principais
- [app/ext/database/__init__.py](app/ext/database/__init__.py)
- [app/ext/configuration/__init__.py](app/ext/configuration/__init__.py)
- [app/ext/migration/__init__.py](app/ext/migration/__init__.py)
- [app/ext/admin/__init__.py](app/ext/admin/__init__.py)

### Blueprint principal
- [app/blueprint/webui/__init__.py](app/blueprint/webui/__init__.py)

### Modelos
- [app/ext/database/models.py](app/ext/database/models.py)

## 🌱 Seeders

O projeto inclui seeders para popular o banco em desenvolvimento:

```bash
flask --app app populate-development
```

Arquivos relevantes:

- [app/seeders/__init__.py](app/seeders/__init__.py)
- [app/seeders/users.py](app/seeders/users.py)
- [app/seeders/bancos.py](app/seeders/bancos.py)
- [app/seeders/categorias.py](app/seeders/categorias.py)
- [app/seeders/entradas.py](app/seeders/entradas.py)
- [app/seeders/saidas.py](app/seeders/saidas.py)
- [app/seeders/saldos.py](app/seeders/saldos.py)
- [app/seeders/faturas.py](app/seeders/faturas.py)
- [app/seeders/compras.py](app/seeders/compras.py)

## 🔁 Deploy automático

O deploy automatizado está configurado em [.github/workflows/deploy.yml](.github/workflows/deploy.yml).

### Fluxo
1. checkout do código;
2. setup do Docker Buildx;
3. login no Docker Hub;
4. build e push da imagem;
5. acesso via SSH ao servidor;
6. execução de:

```bash
docker compose pull
docker compose up -d
```

### Secrets necessárias

- `DOCKERHUB_USERNAME`
- `DOCKERHUB_TOKEN`
- `SSH_HOST`
- `SSH_USER`
- `SSH_KEY`
- `SSH_PORT`

## 🐳 Containerização

O projeto conta com [dockerfile](dockerfile), que usa build em múltiplos estágios e executa a aplicação em porta `5000`.

## 📦 Dependências e lock file

O projeto usa `pip-compile` para gerar o lock final a partir de [requirements.in](requirements.in):

```bash
python -m pip install --upgrade pip pip-tools
pip-compile requirements.in
pip install -r requirements.txt
```

## 🧹 Makefile

Atalhos principais:

```bash
make venv
make requirements
make run
make clear-cache
```

## 📝 Observações

- mantenha `.env` fora do controle de versionamento;
- use SQLite para desenvolvimento e teste local;
- mantenha o `requirements.in` como fonte das dependências;
- gere o `requirements.txt` sempre que houver atualização de pacotes;
- use os seeders para popular o banco em ambiente de desenvolvimento.

---

## 🔗 Projeto

- [README-PT-BR-compact.md](README-PT-BR-compact.md)
- [README-EN.md](README-EN.md)
