from flask_migrate import Migrate, upgrade as migrate_upgrade
import os

from app.ext.database import db
from app.ext.database.models import *
from app import get_base_path

base_path = get_base_path()

def init_app(app):
    migrations_dir = os.path.join(base_path, 'migrations')

    migrate = Migrate(app, db, directory=migrations_dir)

    if os.path.exists(migrations_dir):
        with app.app_context():
            try:
                migrate_upgrade(directory=migrations_dir)
                print("Migrações aplicadas com sucesso.")
            except Exception as e:
                print(f'Erro ao aplicar migrações: {e}')