import os
from pathlib import Path

basedir = Path(__file__).resolve().parent


class Config:
    # Change this in production — set a real SECRET_KEY env var.
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-key-change-me")

    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", f"sqlite:///{basedir / 'instance' / 'ois.db'}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Mail is optional. If MAIL_SERVER is unset, the app still saves every
    # inquiry to the database — it just skips sending the notification email.
    MAIL_SERVER = os.environ.get("MAIL_SERVER")
    MAIL_PORT = int(os.environ.get("MAIL_PORT", 587))
    MAIL_USE_TLS = os.environ.get("MAIL_USE_TLS", "true").lower() == "true"
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = os.environ.get("MAIL_DEFAULT_SENDER", MAIL_USERNAME)

    # Where new-inquiry notification emails get sent.
    ADMIN_EMAIL = os.environ.get("ADMIN_EMAIL", "office@hhskole.dk")
