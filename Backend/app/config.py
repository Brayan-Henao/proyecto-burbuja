import os

from dotenv import load_dotenv


load_dotenv()


class Config:

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SECRET_KEY = os.getenv("SECRET_KEY")

    _db_user = os.getenv("DB_USER", "").strip()
    _db_password = os.getenv("DB_PASSWORD", "").strip()
    _db_host = os.getenv("DB_HOST", "localhost").strip()
    _db_port = os.getenv("DB_PORT", "3306").strip()
    _db_name = os.getenv("DB_NAME", "burbuja_db").strip()

    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{_db_user}:{_db_password}"
        f"@{_db_host}:{_db_port}/{_db_name}"
    )


    # ==========================================
    # WOMPI
    # ==========================================

    WOMPI_PUBLIC_KEY = os.getenv(
        "WOMPI_PUBLIC_KEY"
    )

    WOMPI_PRIVATE_KEY = os.getenv(
        "WOMPI_PRIVATE_KEY"
    )

    WOMPI_EVENTS_SECRET = os.getenv(
        "WOMPI_EVENTS_SECRET"
    )

    WOMPI_INTEGRITY_SECRET = os.getenv(
        "WOMPI_INTEGRITY_SECRET"
    )


    # ==========================================
    # ARCHIVOS SUBIDOS
    # ==========================================

    UPLOAD_FOLDER = os.path.join(
        os.path.dirname(
            os.path.dirname(__file__)
        ),
        "uploads"
    )