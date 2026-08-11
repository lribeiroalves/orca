from dynaconf import FlaskDynaconf


def init_app(app):
    FlaskDynaconf(app=app, settings_files=['config/settings.toml', 'config/secrets.toml'], extensions_list='EXTENSIONS')