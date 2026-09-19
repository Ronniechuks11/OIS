import os

from dotenv import load_dotenv

load_dotenv()  # must run before Config is imported, since it reads os.environ at import time

from flask import Flask

from config import Config
from extensions import csrf, db, mail


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Make sure instance/ exists so SQLite has somewhere to write ois.db.
    os.makedirs(app.instance_path, exist_ok=True)

    db.init_app(app)
    mail.init_app(app)
    csrf.init_app(app)

    from routes import main_bp

    app.register_blueprint(main_bp)

    with app.app_context():
        # Fine for a small SQLite-backed site. If this ever moves to
        # Postgres/MySQL or the schema grows, switch to Flask-Migrate.
        db.create_all()

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
