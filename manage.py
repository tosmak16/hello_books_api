from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from db import db
from app import create_app
from os import environ

app = create_app(environ.get('APP_ENV'))
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()
