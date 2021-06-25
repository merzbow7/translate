from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from app import app, db
from models import Translate

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    t = Translate()
    manager.run()
