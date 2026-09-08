# ORCA

Aplicação web para gestão financeira pessoal com controle de entradas, saídas, saldos, faturas e compras parceladas.

## Visão geral

ORCA é um sistema em Flask com arquitetura modular, usando SQLAlchemy, Flask-Migrate, Dynaconf e Flask-Admin.

### Funcionalidades principais
- cadastro de usuários;
- controle de entradas e saídas;
- gerenciamento de saldos por banco e mês;
- acompanhamento de faturas e compras parceladas;
- administração via painel `/admin`;
- gráficos e relatórios por período;
- suporte a SQLite para desenvolvimento local e Docker para deploy.

## Estrutura do projeto

```text
orca/
├── app/
│   ├── blueprint/
│   ├── ext/
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
├── Makefile
├── dockerfile
├── requirements.in
├── requirements.txt
├── README.md
├── README-PT-BR-compact.md
├── README-EN.md
└── app.py
```

## Requisitos

- Python 3.11+
- pip
- virtualenv
- Git
- Docker (opcional para deploy)

## Configuração local

### 1) Clone e prepare o ambiente

```bash
git clone <url-do-repositorio>
cd orca
python3 -m venv .venv
source .venv/bin/activate
```

### 2) Instale as dependências

```bash
python -m pip install --upgrade pip pip-tools
pip-compile requirements.in
pip install -r requirements.txt
```

Ou use:

```bash
make requirements
```

### 3) Configure o `.env`

Crie um arquivo `.env` na raiz:

```env
FLASK_APP=app
FLASK_ENV=development
FLASK_RUN_HOST=0.0.0.0
FLASK_RUN_PORT=5000
FLASK_DEBUG=1
DYNACONF_SECRET_KEY=troque-por-uma-chave-forte
DYNACONF_SQLALCHEMY_DATABASE_URI=sqlite:////absolute/path/to/orca/instance/database.db
```

Exemplo:

```env
FLASK_APP=app
FLASK_ENV=development
FLASK_RUN_HOST=0.0.0.0
FLASK_RUN_PORT=5000
FLASK_DEBUG=1
DYNACONF_SECRET_KEY=secret-key-local
DYNACONF_SQLALCHEMY_DATABASE_URI=sqlite:////home/seu-usuario/orca/instance/database.db
```

```bash
mkdir -p instance
```

## Execução local

```bash
make run
```

A aplicação ficará disponível em:

```text
http://127.0.0.1:5000
```

## Migrações

O projeto usa Flask-Migrate/Alembic e aplica migrações automaticamente na inicialização da aplicação.

```bash
flask --app app db migrate -m "mensagem"
flask --app app db upgrade
```

## Seeders

Para popular o banco em desenvolvimento:

```bash
flask --app app populate-development
```

## Deploy automático

O pipeline em [/.github/workflows/deploy.yml](.github/workflows/deploy.yml) executa:

1. build da imagem Docker;
2. push para Docker Hub;
3. conexão via SSH no servidor;
4. pull e atualização do container com `docker compose up -d`.

Secrets esperadas:
- `DOCKERHUB_USERNAME`
- `DOCKERHUB_TOKEN`
- `SSH_HOST`
- `SSH_USER`
- `SSH_KEY`
- `SSH_PORT`

## Makefile

Atalhos disponíveis:

```bash
make venv
make requirements
make run
make clear-cache
```

## Observações

- use SQLite para desenvolvimento local;
- mantenha `.env` fora do controle de versão;
- mantenha `requirements.in` como origem das dependências;
- gere `requirements.txt` com `pip-compile` sempre que atualizar pacotes.

---

## Referências

- [README.md](README.md)
- [README-EN.md](README-EN.md)
