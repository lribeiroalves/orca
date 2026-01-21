# Variáveis para facilitar mudanças futuras
PYTHON = python3
APP_FILE = src/main.py

.PHONY: run install requirements clean

# Comando principal: basta digitar 'make' ou 'make run'
run:
	flet run --android $(APP_FILE) -d

# Atalho para instalar dependências
install:
	pip install -r requirements.txt

# Atalho para criar o requirements
requirements:
	pip freeze > requirements.txt

# Atalho para limpar arquivos temporários do Python
clean:
	rm -rf __pycache__ .pytest_cache

# Atalho para compilar o apk
apk:
	flet build apk src  --project "ORCA Financas"  --org "com.lucas.orca"  --product "ORCA"  --description "Gestao Financeira Familiar"  --clear-cache

