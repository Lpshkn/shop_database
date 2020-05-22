from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from app.context_procesor import add_icon_path, sort_icon_path

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'

app.context_processor(add_icon_path)
app.context_processor(sort_icon_path)
app.jinja_env.globals.update(add_icon=add_icon_path)
app.jinja_env.globals.update(sort_icon=sort_icon_path)


from app import routes
