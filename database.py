from flask_sqlalchemy import SQLAlchemy
from server import generate_app

db = SQLAlchemy(generate_app())
