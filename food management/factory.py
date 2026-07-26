from flask import Flask
from flask_jwt_extended import JWTManager
from os import environ
from models.user import db
from flask_migrate import Migrate

def create_app():
    app = Flask(__name__)

    # เปลี่ยนจาก MONGO_URL เป็น MySQL connection string
    db_user = environ.get("DB_USER", "root")
    db_pass = environ.get("DB_PASS", "m1827")
    db_host = environ.get("DB_HOST", "localhost")
    db_port = environ.get("DB_PORT", "3306")
    db_name = environ.get("DB_NAME", "food_inventory_db")

    app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"mysql+pymysql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = environ.get('JWT_SECRET_KEY', 'secret123')

    db.init_app(app)
    JWTManager(app)
    Migrate(app, db)

    from routes.auth import bp
    app.register_blueprint(bp)

    return app