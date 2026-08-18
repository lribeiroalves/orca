from flask_migrate import Migrate, upgrade as migrate_upgrade
from alembic.script import ScriptDirectory
from alembic.config import Config
from alembic.runtime.migration import MigrationContext
from sqlalchemy import create_engine

import os

from app.ext.database import db
from app.ext.database.models import *
from app import get_base_path

base_path = get_base_path()
migrations_dir = os.path.join(base_path, 'migrations')


def banco_atualizado(db_url):
    alembic_cfg = Config(os.path.join(migrations_dir, 'alembic.ini'))
    alembic_cfg.set_main_option("script_location", migrations_dir)
    script = ScriptDirectory.from_config(alembic_cfg)
    head = script.get_current_head()

    engine = create_engine(db_url)
    with engine.connect() as conn:
        context = MigrationContext.configure(conn)
        current = context.get_current_revision()

    return current == head


def init_app(app):
    migrate = Migrate(app, db, directory=migrations_dir)

    if os.path.exists(migrations_dir):
        with app.app_context():
            try:
                if not banco_atualizado(app.config['SQLALCHEMY_DATABASE_URI']):
                    migrate_upgrade(directory=migrations_dir)
                    print("Migrações aplicadas com sucesso.")
                else:
                    print('Banco atualizado!')
            except Exception as e:
                print(f'Erro ao aplicar migrações: {e}')