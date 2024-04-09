from flask import Flask
from flask_cors import CORS
from config import Config
from flask_sqlalchemy import SQLAlchemy


# instantiate the app
app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})


from app import routes, models, parse

